from machine import Pin
from time import sleep_ms
from servo import Servo
from math import sin, radians


servo = Servo(Pin(6))


print('''
Test Servo:
Moves servo motor in a sinusoidal way.
Press Ctrl+C to exit test.
''')
try:
    while True:
        for i in range(360):
            servo.set_angle(sin(radians(i + 90)) * 90 + 90)
            sleep_ms(5)
except KeyboardInterrupt:
    pass
servo.set_enable(False)
print('''
Done!
Can press ctrl-d to soft-reset.
''')
