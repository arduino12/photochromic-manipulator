try:
    from espnow import ESPNow
except ImportError:
    print('''
Failed to import espnow!
Please use MicroPython v1.20 with espnow:
https://github.com/glenn20/micropython-espnow-images/blob/main/20230427-v1.20.0-espnow-2-gcc4c716f6/firmware-esp32-LOLIN_S2_MINI.bin
Or the latest MicroPython version:
https://micropython.org/resources/firmware/LOLIN_S2_MINI-20230623-unstable-v1.20.0-243-gd93316fe3.bin
''')
    raise SystemExit()
from sys import modules, stdin, stdout
from network import WLAN, STA_IF
from select import poll, POLLIN
from time import sleep, sleep_ms
from machine import unique_id
from pm import PM
from ansi import *
from rgb_leds import RgbColor
try:
    from secrets import USERNAME
except ImportError:
    USERNAME = None


class EspNowChat:
    _BROADCAST_ADDRESS = b'\xff\xff\xff\xff\xff\xff'
    _SEP = '\n'
    _PROMPT = sgr_text('> ', SGR_GREEN, SGR_BOLD)
    _NAME = sgr(SGR_MAGENTA, SGR_BOLD)
    _NAME_SEP = sgr_text('> ', SGR_NORMAL, SGR_MAGENTA + SGR_BRIGHT)
    _BAD_CMD = sgr_text('No such command! see /help', SGR_RED, SGR_BOLD)
    _HELP = '''
{1}ESP-NOW Chat V1.0.0{0}
 {2}/help\t{3}Print this help message.
 {2}/beep\t{4}<freq=440> <username=you> {3}Beep a user buzzer.
 {2}/led\t{4}<color=black> <username=you> {3}Set a user LED color.
 {3}Any other text will be sent to all chat users.
{5}Press ctrl-c to exit.{0}
'''.format(SGR_END, sgr(SGR_GREEN, SGR_BOLD, SGR_UNDERLINE),
           sgr(SGR_YELLOW, SGR_BOLD), sgr(SGR_NORMAL, SGR_CYAN + SGR_BRIGHT),
           sgr(SGR_NOT_BOLD), sgr(SGR_RED, SGR_BOLD))

    def __init__(self):
        self._name = USERNAME.replace(self._SEP, '_').replace(' ', '_') \
                     if USERNAME else unique_id().hex()[8:]
        sta = WLAN(STA_IF) # A WLAN interface must be active for espnow
        sta.active(True)
        sta.disconnect()
        self._espnow = ESPNow()
        self._espnow.active(True)
        self._espnow.config(timeout_ms=0, buffer=263*10) # rxbuf=buffer
        self._espnow.add_peer(self._BROADCAST_ADDRESS)
        self._ipoll = poll()
        self._ipoll.register(stdin, POLLIN)
        self._pm = PM()

    def _nonblocking_input(self):
        line = '' # Thonny IDE shell is bufferd- user input is sent only after ENTER is pressed
        while self._ipoll.poll(0): # so once STDIN is readable - we got new input to return
            line += stdin.read(1)
        if not line:
            return None
        line = line.strip()
        print(line, end='')
        return line

    def _input_prompt(self, is_on):
        print('\r\r', end=self._PROMPT if is_on else '')

    def _espnow_send(self, msg):
        self._espnow.send(self._BROADCAST_ADDRESS, self._name + self._SEP + msg)

    def _cmd_help(self, *args):
        print(self._HELP)

    def _cmd_led(self, caller, color='black', username=None):
        print(caller, color, username)
        self._pm.rgb_leds.fill(color)

    def _handle_command(self, caller, line):
        args = line.split()
        cmd = args.pop(0).replace('/', '_cmd_')
        args.insert(0, caller)
        getattr(self, cmd, lambda *x: print(self._BAD_CMD))(*args)

    def _handle_espnow(self):
        for mac, msg in self._espnow:
            if mac is None:
                break
            msg = msg.decode().split(self._SEP)
            if len(msg) < 2:
                continue
            self._input_prompt(False)
            if msg[1].startswith('/'):
                self._handle_command(*msg)
            else:
                print(self._NAME, msg[0], self._NAME_SEP, msg[1], sep='')
            self._input_prompt(True)

    def _handle_terminal(self):
        text = self._nonblocking_input()
        if text is not None:
            if text.startswith('/'):
                self._input_prompt(False)
                self._handle_command(self._name, text)
                self._input_prompt(True)
            elif text:
                self._espnow_send(text)
            self._input_prompt(True)

    def loop(self):
        self._input_prompt(False)
        self._cmd_help()
        self._input_prompt(True)
        try:
            while True:
                self._handle_espnow()
                self._handle_terminal()
                sleep_ms(10)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    enc = EspNowChat()
    enc.loop()


modules.clear() # make sure we can re-import the example!
print('''
Done!
Can press ctrl-d to soft-reset.
''')