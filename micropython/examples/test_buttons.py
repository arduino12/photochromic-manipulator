from machine import Pin
from time import sleep_ms


btn_b = Pin(0, Pin.OUT, drive=Pin.DRIVE_0, value=1) # PULL_UP doesn't pull enough..
btn_l = Pin(12, Pin.PULL_UP)
btn_r = Pin(34, Pin.PULL_UP) # can also work with pin 4 if it is soldered to pin 34.


print("""
Test Buttons:
Prints button states (pressed=0, released=1).
Press ctrl-c to exit test.
""")
try:
    while True:
        b = btn_b.value()
        l = btn_l.value()
        r = btn_r.value()
        print("B=", b, " L=", l, " R=", r, end="\t\t\r", sep="") # print over the same line
        sleep_ms(20)
except KeyboardInterrupt:
    pass
print("""
Done!
Can press ctrl-d to soft-reset.
""")
