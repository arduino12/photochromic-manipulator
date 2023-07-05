#
# FBM = Five Bars Manipulator: quick and dirty driver for PM kit V2.
#
# https://github.com/arduino12/photochromic_manipulator 2023/07/05
#
from sys import modules
from math import sqrt, degrees, asin, acos, floor
from time import sleep, sleep_ms
from pm import PM

__version__ = '0.0.1'

class FBM(object):

    HOME_POINT = (0, 15)
    _SERVO_OFFSET = 45
    X_MIN, X_MAX, Y_MIN, Y_MAX = -35, 35, 15, 65

    def __init__(self, bar0=16, bar1=34, bar2=43):
        self._bar0 = bar0
        self._bar1 = bar1
        self._bar2 = bar2
        self.draw_speed = 3
        self.move_speed = 3
        self._next_points = []
        self._next_x = []
        self._next_y = []
        self._next_z = []
        self.pm = PM()
        self._last_x = self.HOME_POINT[0]
        self._last_y = self.HOME_POINT[1] + 30 # so it will go home
        self.auto_draw = True
        self.move_home()

    def set_led(self, draw):
        if draw is None:
            return
        self.pm.uv_led.value(draw)

    def set_axes(self, left_angle, right_angle):
        self.pm.servo_l.set_angle(left_angle - self._SERVO_OFFSET)
        self.pm.servo_r.set_angle(right_angle + self._SERVO_OFFSET)

    def set_axes_fbk(self, x, y):
        if x < self.X_MIN or y < self.Y_MIN or x > self.X_MAX or y > self.Y_MAX:
            return False

        half_b0 = self._bar0 / 2;
        l_x = x + half_b0
        r_x = x - half_b0

        yy = y ** 2
        l_ss = l_x ** 2 + yy
        r_ss = r_x ** 2 + yy

        l_s = sqrt(l_ss);
        r_s = sqrt(r_ss);

        l_a = degrees(asin(y / l_s));
        r_a = degrees(asin(y / r_s));

        if l_x <= 0:
            l_a = 180 - l_a;

        if r_x >= 0:
            r_a = 180 - r_a;

        bb1 = 2 * self._bar1
        b1b2 = self._bar1 ** 2 - self._bar2 ** 2

        l_a += degrees(acos((b1b2 + l_ss) / (bb1 * l_s)));
        r_a += degrees(acos((b1b2 + r_ss) / (bb1 * r_s)));

        r_a = 180 - r_a;

        self.set_axes(l_a, r_a)

    def _move_to(self, p_x, p_y, speed):
        d_x = p_x - self._last_x
        d_y = p_y - self._last_y

        # path lenght in mm, times 4 equals 4 steps per mm
        c = floor(10 * sqrt(d_x * d_x + d_y * d_y));
        if c < 1:
            c = 1

        # draw line point by point
        for i in range(c + 1):
            self.set_axes_fbk(self._last_x + (i * d_x / c), self._last_y + (i * d_y / c))
            sleep_ms(speed);

        self.set_axes_fbk(p_x, p_y);
        self._last_x = p_x;
        self._last_y = p_y;
        sleep_ms(speed);

    def update_blocking(self):
        while self._next_z:
            x = self._next_x.pop(0)
            y = self._next_y.pop(0)
            z = self._next_z.pop(0)
            self.set_led(z)
            s = self.draw_speed if self.pm.uv_led.value() else self.move_speed
#             print(x, y, z, s)
            self._move_to(x, y, s)
        self.stop()

    def stop(self, draw=False):
        self.set_led(draw)
        self.pm.servo_l.set_enable(False)
        self.pm.servo_r.set_enable(False)
        self._next_x.clear()
        self._next_y.clear()
        self._next_z.clear()
#         collect() # free unuesed RAM!

    def goto(self, point, draw=None):
        self._next_x.append(point[0])
        self._next_y.append(point[1])
        self._next_z.append(draw)
        if self.auto_draw:
            self.update_blocking()

    def move_home(self, immediately=False):
        if immediately:
            self.stop()
        self.goto(self.HOME_POINT, False)

    def draw_line(self, p1, p2):
        self.goto(p1, False)
        self.goto(p2, True)

    def draw_poly(self, points, closed=True):
        self.goto(points[0], False)
        for p in points[1:]:
            self.goto(p, True)
        if closed:
            self.goto(points[0], True)

    def get_drawing_rect(self, scale):
        if not self._next_z:
            return self.X_MIN, self.X_MAX, self.Y_MIN, self.Y_MAX
        return min(self._next_x), max(self._next_x), min(self._next_y), max(self._next_y)

    def drawing_transform(self, func_x, func_y):
        for i in range(len(self._next_z)):
            self._next_x[i] = func_x(self._next_x[i])
            self._next_y[i] = func_y(self._next_y[i])

    def drawing_scale(self, scale):
        self.drawing_transform(lambda x, y: (x * scale, y * scale))
        for i in range(len(self._next_z)):
            self._next_x[i] *= scale
            self._next_y[i] *= scale

    def set_enable(self, is_enabled):
        self.stop()
        self.pm.set_enable(is_enabled)


if __name__ == '__main__':
    print('\nTest fbm', __version__)

    try:
        fbm = FBM()
        fbm.move_home()
        Y = 20
        W, H = 8, 16
        for i in range(5):
            fbm.draw_poly(((-W, Y), (W, Y), (W, Y+H), (-W, Y+H)))
        fbm.move_home()
    except KeyboardInterrupt:
        pass

    fbm.set_enable(False)

modules.clear() # make sure we can re-import the example!
print('''
Done!
Can press ctrl-d to soft-reset.
''')
