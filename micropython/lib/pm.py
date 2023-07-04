#
# pm.py - micropython library for Photochromic Manipulator V2 kit.
#
# ESP32-S2-Mini controlls:
#  2 Servo motors.
#  2 NeoPixel LEDs.
#  1 UV LED.
#  1 Blue LED.
#  1 Piezoelectric buzzer.
#  3 Push-Buttons (1 boot, 2 also capacitive touch pads).
#  1 Digital temperature sensor.
#  1 IR receiver (interrupt based- not very reliable..).
#  1 IR LED (externally connected to enable transmitting IR codes).
#  1 WiFi (can do remote REPL).
#
# https://github.com/arduino12/photochromic_manipulator 2023/07/04
#

__version__ = '1.0.0'

from micropython import const
from machine import Pin, Timer #, TouchPad
from buzzer import Buzzer
from servo import Servo
from gc import collect
from rgb_leds import RgbLeds
from utils import init_timer_collect
from ir_nec import IR_RX_NEC, IR_TX_NEC


HW_VERSION = const(2)
SW_VERSION = const(1)

SDA_PIN = const(8)
SCL_PIN = const(10)
BTN_B_PIN = const(0)
BTN_L_PIN = const(12) # Touch-Pads pins can be 1-14!
BTN_R_PIN = const(4) # PCB V2 connected to pin 34 so need bridging to pin 4!
UV_LED_PIN = const(33)
SERVO_L_PIN = const(7)
SERVO_R_PIN = const(6)
BUZZER_A_PIN = const(11)
BUZZER_B_PIN = const(13)
NEOPIXEL_PIN = const(9)
BLUE_LED_PIN = const(15)
IR_RECEIVER_PIN = const(14)
IR_TRANSMITTER_PIN = const(21) # need to connect external IR LED!


class PM:

    def __init__(self):
        self.rgb_leds = RgbLeds(Pin(NEOPIXEL_PIN))
        self.uv_led = Pin(UV_LED_PIN, Pin.OUT)
        self.blue_led = Pin(BLUE_LED_PIN, Pin.OUT)
        self.buzzer = Buzzer(Pin(BUZZER_A_PIN), Pin(BUZZER_B_PIN))
        self.servo_l = Servo(Pin(SERVO_L_PIN))
        self.servo_r = Servo(Pin(SERVO_R_PIN))
        # self.touch_l = TouchPad(Pin(BTN_L_PIN))
        # self.touch_r = TouchPad(Pin(BTN_R_PIN))
        self.btn_l = Pin(BTN_L_PIN, Pin.OUT, drive=Pin.DRIVE_0, value=1)
        self.btn_r = Pin(BTN_R_PIN, Pin.OUT, drive=Pin.DRIVE_0, value=1)
        self.btn_b = Pin(BTN_B_PIN, Pin.OUT, drive=Pin.DRIVE_0, value=1) # PULL_UP doesn't pull enough..
        self.ir_receiver = IR_RX_NEC(Pin(IR_RECEIVER_PIN))
        self.ir_transmitter = IR_TX_NEC(Pin(IR_TRANSMITTER_PIN), active_level=False)
        self.timer_collect = init_timer_collect()


if __name__ == '__main__':
    pm = PM()
