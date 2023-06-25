from machine import Pin
from time import sleep_ms
from thermometer import Thermometer


thermometer = Thermometer(1, Pin(10), Pin(8))


print('''
Test Thermometer:
Prints temperature readings over the same line.
Press Ctrl+C to exit test.
''')
try:
    while True:
        print(thermometer.read_temp_str_c(), end='\t\r', sep='')
        sleep_ms(500)
except KeyboardInterrupt:
    pass

print('''
Done!
Can press ctrl-d to soft-reset.
''')
