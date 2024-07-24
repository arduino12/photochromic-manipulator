from sys import modules
from random import randrange
from time import sleep_ms, time
from pm import PM
from ansi import *


_LOG_I = sgr(SGR_WHITE)
_LOG_W = sgr(SGR_YELLOW, SGR_BOLD)
_LOG_E = sgr(SGR_RED, SGR_BOLD)
_LOG_G = sgr(SGR_GREEN, SGR_BOLD)
_TEST = sgr(SGR_CYAN, SGR_BOLD)
_PROMPT = sgr_text('Test[{:02}]> ', SGR_BLUE, SGR_BOLD)
_PR_FMT = 'P[{1}{{}}{0}] R[{1}{{}}{0}] T[{1}{{}}{0}]'.format(SGR_END, _LOG_W)
_test_id = 1


pm = PM()


def test_log(_sgr, line, end='\n'):
    print(_test_prompt, _sgr, line, SGR_END, sep='', end=end)


def test_start(line):
    global _test_prompt
    _test_prompt = _PROMPT.format(_test_id)
    test_log(_TEST, line)


def test_end(error_id):
    global _test_id
    test_log(_LOG_E if error_id else _LOG_G,
             'Failed!' if error_id else 'Passed!', end='\n\n')
    _test_id += 1


print('''
Test Peripherals:
Performs a hardware self test for this PCB.
Press Ctrl-C to exit the test.
''')
try:
    ret = 0
    test_start('IR')
    ir_tx_byte = randrange(256)
    test_log(_LOG_I, 'Sent NEC code 0x{:02x}'.format(ir_tx_byte))
    pm.ir_tx.transmit(ir_tx_byte)
    sleep_ms(200)
    if pm.ir_rx.received():
        ir_rx_byte, _ = pm.ir_rx.get()
        if ir_rx_byte == ir_tx_byte:
            test_log(_LOG_I, 'Received correct NEC code 0x{:02x}'.format(ir_rx_byte))
            ret = 0
        else:
            test_log(_LOG_W, 'Received incorrect NEC code 0x{:02x}'.format(ir_rx_byte))
            ret = 1
    else:
        test_log(_LOG_E, 'No NEC code was received!')
        ret = 2
    test_end(ret)

    test_start('Thermometer')
    try:
        temp = pm.thermometer.read_temp_c()
    except Exception:
        test_log(_LOG_E, 'No thermometer was detected!')
        ret = 2
    else:
        if 10 <= temp <= 50:
            test_log(_LOG_I, 'Thermometer read {0:.2f}°C'.format(temp))
            ret = 0
        else:
            test_log(_LOG_W, 'Thermometer read out of range {0:.2f}°C'.format(temp))
            ret = 1
    test_end(ret)

    def pr_test(l_func, r_func):
        global ret
        LR = ('LR', ' R', 'L ', '  ')
        ret = 0b1111
        t = 8
        stop_time = time() + t
        while ret and t:
            t = stop_time - time()
            ret &= 0b1011 if l_func() else 0b1110
            ret &= 0b0111 if r_func() else 0b1101
            test_log(_LOG_I,
                     _PR_FMT.format(LR[ret & 3], LR[ret // 4], t),
                     end='\t\t\t\t\t\r')
            sleep_ms(20)
        print()

    test_start('Buttons')
    test_log(_LOG_G, 'Press and release the 2 black buttons...')
    pr_test(pm.btn_l.value, pm.btn_r.value)
    test_end(ret)

    test_start('Touchpads')
    test_log(_LOG_G, 'Press and release the 2 PCB touchpads...')
    l_th = int(pm.touch_l.read() * 1.12)
    r_th = int(pm.touch_r.read() * 1.12)
    pr_test(lambda: pm.touch_l.read() < l_th, lambda: pm.touch_r.read() < r_th)
    test_end(ret)

    test_start('RGB LEDs and buzzer')
    test_log(_LOG_W, 'Verify LEDs red, green and blue colors and buzzer beeps...')
    for i in range(3):
        pm.buzzer.beep(440 + i * 440)
        for c in ('red', 'green', 'blue'):
            pm.rgb_leds.fill(c)
            sleep_ms(500)
    pm.rgb_leds.off()
    pm.buzzer.off()

except KeyboardInterrupt:
    pass
pm.set_enable(False)
modules.clear() # make sure we can re-import the example!
print('''
Done!
Can press Ctrl-D to soft-reset.
''')
