#
# utils.py - MicroPython library for common stuff.
#
# https://github.com/arduino12/micropython-libs 2023/07/04
#

__version__ = '1.0.0'

from machine import Timer
from gc import collect


def init_timer_collect(seconds=60):
    return Timer(-1, period=seconds * 1000, mode=Timer.PERIODIC, callback=lambda _: collect())
