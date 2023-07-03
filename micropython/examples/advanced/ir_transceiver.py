from sys import modules
from gc import collect
from machine import Pin, Timer
from time import time, sleep, sleep_ms
from buzzer import Buzzer
from neopixel import NeoPixel
from ir_nec import IR_RX_NEC, IR_TX_NEC


ir_rx = IR_RX_NEC(Pin(14)) # IR receiver VS1838B
ir_tx = IR_TX_NEC(Pin(33)) # IR LED need to connect externally
rgb_leds = NeoPixel(Pin(9), 2)
buzzer = Buzzer(Pin(11), Pin(13))
btn_l = Pin(12, Pin.OUT, drive=Pin.DRIVE_0, value=1) # PULL_UP doesn't pull enough..
btn_r = Pin(34, Pin.OUT, drive=Pin.DRIVE_0, value=1)
timer = Timer(-1)


def set_leds_color(c):
    rgb_leds.fill((
        128 if c & 1 else 0,
        128 if c & 2 else 0,
        128 if c & 4 else 0
    ))
    rgb_leds.write()


def beep(freq, duration=100):
    buzzer.set_freq(freq)
    timer.init(period=duration, mode=Timer.ONE_SHOT, callback=lambda t: buzzer.set_freq(0))


last_c = 0
print('''
IR Transceiver - each button press sends an IR NEC signal,
received IR NEC signals sets the LEDs color and buzzer beeps.
Press ctrl-c to exit test.
''')
try:
    while True:
        c = (not btn_l.value()) * 1 + (not btn_r.value()) * 2
        if c and c != last_c:
            print('Transmited IR address: ', c)
            ir_tx.transmit(c)
        last_c = c
            
        if ir_rx.received():
            c, _ = ir_rx.get()
            print('Received IR address: ', c)
            set_leds_color(c)
            beep(440 * c)

        sleep_ms(10)
except KeyboardInterrupt:
    pass
buzzer.set_freq(0)
set_leds_color(0)
modules.clear() # make sure we can re-import the example!
print('''
Done!
Can press ctrl-d to soft-reset.
''')
