#
# buzzer.py - MicroPython library for driving a piezoelectric buzzer.
# Supports single-pin PWM (buzzer conected to a GPIO and GND),
# and dual-pin complementary PWM (buzzer conected to both GPIOs) - louder than single-pin.
#
# https://github.com/arduino12/micropython-libs 2023/06/17
#

__version__ = '1.0.0'

from machine import Pin, PWM, mem32
from micropython import const
from sys import platform


# see page 186 of https://www.espressif.com/sites/default/files/documentation/esp32-s2_technical_reference_manual_en.pdf
_GPIO_FUNCn_OUT_SEL_CFG_REG = const(0x3F404554) #  (n: 0-53) (0x3F404000+0x0554+4*n)
_GPIO_FUNCn_OUT_INV_SEL = const(1 << 9)


class Buzzer:

    def __init__(self, a_pin, b_pin=None):
        # create a PWM for the given a_pin at 50% duty-cycle
        self._pwm = PWM(a_pin, duty_u16=0)
        
        # if b_pin is given, output an inverted PWM signal to it!
        # louder buzzer output compared to connecting b_pin to GND.
        if b_pin is not None:
            if platform == 'esp32':
                pn = lambda x: int(str(x)[4:-1]) # get pin number from Pin object
                # ESP32 GPIO matrix register magic!
                mem32[_GPIO_FUNCn_OUT_SEL_CFG_REG + 4 * pn(b_pin)] =\
                mem32[_GPIO_FUNCn_OUT_SEL_CFG_REG + 4 * pn(a_pin)] |\
                _GPIO_FUNCn_OUT_INV_SEL
            else:
                # TODO: add support for RP2040, ESP8266...
                raise NotImplementedError('inverted PWM signal not implemented for this platform!')

    def set_freq(self, freq_hz):
        if freq_hz:
            self._pwm.init(freq=freq_hz, duty_u16=0x8000)
        else:
            self._pwm.duty_u16(0)


if __name__ == '__main__':
    print('\nTest buzzer', __version__)

    from machine import Pin
    from time import sleep_ms

    buzzer = Buzzer(Pin(2), Pin(3))

    try:
        for i in range(6):
            buzzer.set_freq(880 if i % 2 else 440)
            sleep_ms(500)
    except KeyboardInterrupt:
        pass

    buzzer.set_freq(0)
