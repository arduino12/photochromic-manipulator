from machine import Pin, TouchPad
from time import sleep_ms


touch_l = TouchPad(Pin(12)) # Touch-Pads pins can be 1-14!
touch_r = TouchPad(Pin(4)) # PCB V2 connected to pin 34 so need soldering to pin 4!

print("""
Test Touch:
Prints touch-pads states (pressed=large value, released=small value).
Press Ctrl+C to exit test.
""")
try:
    while True:
        l = touch_l.read()
        r = touch_r.read()
        print("L=", l, " R=", r, end="\t\t\r", sep="") # print over the same line
        sleep_ms(20)
except KeyboardInterrupt:
    pass
print("""
Done!
Can press ctrl-d to soft-reset.
""")
