#
# utils.py - MicroPython library for common stuff.
#
# https://github.com/arduino12/micropython-libs 2023/07/04
#

__version__ = '1.0.0'

from machine import Timer
from gc import collect


_timer_collect = Timer(-1)


def set_timer_collect(is_enabled, seconds=60):
    if is_enabled:
        _timer_collect.init(period=seconds * 1000, mode=Timer.PERIODIC,
                            callback=lambda _: collect())
    else:
        _timer_collect.deinit()
