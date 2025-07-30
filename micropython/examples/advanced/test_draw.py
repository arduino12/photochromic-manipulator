from sys import modules
from time import sleep
from pm import PM


class Draw:

    _HEART_POLY = [
        (-26, 42), (-21, 43), (-17, 43), (-8, 41), (-3, 42), (2, 46),
        (5, 52), (5, 58), (2, 60), (-1, 58), (-2, 56), (-3, 55), (-4, 57),
        (-6, 59), (-9, 59), (-11, 57), (-11, 54), (-9, 50), (4, 41), (14, 44),
        (16, 47), (17, 50), (16, 52), (14, 53), (12, 51), (11, 52), (9, 53),
        (7, 51), (8, 48), (12, 43), (20, 41), (24, 43), (29, 42), (34, 40)]

    def __init__(self, pm=None):
        self._pm = pm or PM(move_home=True)

    def _begin(self, draw_speed=0, move_speed=0, led_ms=5):
        self._draw_speed = self._pm.draw_speed
        self._move_speed = self._pm.move_speed
        self._led_ms = self._pm.led_ms
        self._pm.draw_speed = draw_speed
        self._pm.move_speed = move_speed
        self._pm.led_ms = led_ms

    def _end(self, return_home=True):
        if return_home:
            self._pm.move_home()
        self._pm.draw_speed = self._draw_speed
        self._pm.move_speed = self._move_speed
        self._pm.led_ms = self._led_ms

    def squid_game_logo(self, **kw):
        self._begin()
        R, S, Y = 8, 7, 40
        X = R * 2 + S
        self._pm.draw_circle(-X, Y, R)
        self._pm.draw_regular_poly(0, Y, R * 1.4, 3, 210)
        self._pm.draw_rect(X, Y + 2, R * 2)
        self._end(**kw)

    def centered_squares(self, **kw):
        self._begin()
        for i in range(3):
            size = 16 + i * 4
            self._pm.draw_rect(0, 40, size)
        self._end(**kw)

    def centered_hexagon(self, **kw):
        self._begin()
        self._pm.draw_regular_poly(0, 40, 20, 6)
        self._end(**kw)

    def centered_hexagon(self, **kw):
        self._begin()
        self._pm.draw_regular_poly(0, 40, 20, 6)
        self._end(**kw)

    def heart_line(self, **kw):
        self._begin()
        self._pm.rgb_leds.fill('red')
        self._pm.draw_poly(self._HEART_POLY, False)
        self._pm.rgb_leds.off()
        self._end(**kw)

    def star_of_david(self, **kw):
        self._begin()
        self._pm.rgb_leds.fill('blue')
        self._pm.draw_regular_poly(0, 42, 14, 3, 210)
        self._pm.draw_regular_poly(0, 42, 14, 3, 30)
        self._pm.draw_line((-35, 60), (35, 60))
        self._pm.draw_line((35, 24), (-35, 24))
        self._pm.rgb_leds.off()
        self._end(**kw)

    def mabat_logo(self, **kw):
        self._begin(led_ms = 0)
        Y, W, H, S, A = 40, 32, 38, 5, 4
        self._pm.rgb_leds.fill('yellow')
        self._pm.buzzer.play_rtttl_song('Mission Impossible', blocking=False)
        self._pm.draw_circle(0, Y, 3)
        for i in range(3):
            self._pm.rgb_leds.fill(0xff << (8 * i))
            self._pm.draw_ellipse(0, Y, 16, 6, 30 + 120 * i)
        self._pm.rgb_leds.fill('cyan')
        self._pm.draw_circle(0, Y, 18)
        self._pm.rgb_leds.fill('magenta')
        self._pm.draw_quadratic_bezier_curve((W, Y-S), (0, Y-H), (-W, Y-S))
        self._pm.draw_regular_poly(-W, Y-S, A, 3, 20)
        self._pm.draw_quadratic_bezier_curve((-W, Y+S), (0, Y+H), (W, Y+S))
        self._pm.draw_regular_poly(W, Y+S, A, 3, 200)
        self._pm.rgb_leds.off()
        self._end(**kw)

    def israel_flag(self, **kw):
        self._begin(draw_speed=1, led_ms=15)
        self._pm.buzzer.play_rtttl_song('Hatikvah', blocking=False)
        for i in range(2):
            self._pm.rgb_leds.fill('cyan')
            self._pm.draw_regular_poly(0, 42, 14, 3, 210)
            self._pm.rgb_leds.fill('blue')
            self._pm.draw_regular_poly(0, 42, 14, 3, 30)
            if i:
                break
            self._pm.rgb_leds.fill('white')
            self._pm.draw_line((-35, 60), (35, 60))
            self._pm.draw_line((35, 24), (-35, 24))
        self._pm.move_home()
        sleep(4)
        self._pm.rgb_leds.off()
        self._end(**kw)

    def yellow_ribbon(self, **kw):
        self._begin(draw_speed=0)
        self._pm.rgb_leds.fill('yellow')
        self._pm.buzzer.play_rtttl_song('Toccata', blocking=False)
        self._pm.draw_quadratic_bezier_curve((-8, 64), (-10, 58), (-7, 55))
        self._pm.draw_poly(((-7, 55), (12, 30), (7, 25), (-12, 50)), False)
        self._pm.draw_cubic_bezier_curve((-12, 50), (-20, 70), (20, 70), (12, 50))
        self._pm.draw_line((12, 50), (5, 40))
        self._pm.draw_poly(((0, 35), (-7, 25), (-12, 30), (-5, 40)), False)
        self._pm.draw_line((0, 47), (7, 55))
        self._pm.draw_quadratic_bezier_curve((7, 55), (10, 58), (8, 64))
        self._pm.draw_quadratic_bezier_curve((7, 55), (0, 65), (-7, 55))
        self._pm.move_home()
        sleep(2)
        self._pm.rgb_leds.off()
        self._end(**kw)

pm=None
def main():
    global pm
    draw = Draw()
    pm = draw._pm
    drawings = [i for i in dir(draw) if not i.startswith('_')]
    draw_index = 0
    last_btn = 0
    print('''
Test drawings!
Press buttons to draw next or previous drawing. 
Press Ctrl-C to exit.
    ''')
    try:
        draw.yellow_ribbon(); raise KeyboardInterrupt()
        while True:
            btn = (not pm.btn_l.value()) * 1 + (not pm.btn_r.value()) * 2
            if btn and btn != last_btn:
                if btn == 1:
                    draw_index = draw_index + 1 if draw_index < len(drawings) - 2 else 0
                elif btn == 2:
                    draw_index = draw_index - 1 if draw_index else len(drawings) - 1
                draw_name = drawings[draw_index]
                print('Drawing:', draw_name)
                getattr(draw, draw_name)()
            last_btn = btn
    except KeyboardInterrupt:
        pass
    pm.set_enable(False)
    modules.clear() # make sure we can re-import the example!
    print('''
Done!
Can press Ctrl-D to soft-reset.
    ''')


if __name__ == '__main__':
    main()
