#
# FBM = Five Bars Manipulator: quick and dirty driver for PM kit V2.
#
# https://github.com/arduino12/photochromic_manipulator 2023/07/05
#
from sys import modules
from math import degrees, sin, cos
from time import sleep, sleep_ms
from fbm import FBM
from ansi import *


fbm = FBM()


print('''
{1}Photochromic manipulator calibration!:{0}
{2}Press 'A' pushbutton to set motors 90 degrees-
Connect the arms and screw them to the motors.{0}
{3}Press 'B' pushbutton to draw test patterns.{0}

{4}Press Ctrl-C to exit.{0}
'''.format(SGR_END, sgr(SGR_GREEN, SGR_BOLD, SGR_UNDERLINE),
           sgr(SGR_YELLOW, SGR_BOLD), sgr(SGR_CYAN, SGR_BOLD),
           sgr(SGR_RED, SGR_BOLD)))
fbm.move_home()
last_c = 0
try:
    while True:
        c = (not fbm.pm.btn_l.value()) * 1 + (not fbm.pm.btn_r.value()) * 2
        if c and c != last_c:
            print('Press:', c)
            if c == 1:
                fbm._move_to(0, 48, 6)
            elif c == 2:
                fbm.move_home()
                Y = 20
                W, H = 8, 16
                for i in range(3):
                    fbm.draw_poly(((-W, Y), (W, Y), (W, Y + H), (-W, Y + H)))
                fbm.move_home()
        last_c = c
except KeyboardInterrupt:
    pass
fbm.set_enable(False)
modules.clear() # make sure we can re-import the example!
print('''
Done!
Can press Ctrl-D to soft-reset.
''')
