from sys import modules
from machine import Pin
from time import sleep_ms
from ir_nec import IR_RX_NEC, IR_TX_NEC


ir_receiver = IR_RX_NEC(Pin(14)) # IR receiver VS1838B
ir_transmitter = IR_TX_NEC(Pin(33)) # IR LED need to connect externally


print('''
Test IR NEC protocol transmission and reception:
Transmit counter value every half a second.
Print received values.
''')
try:
    ir_receiver.set_callback(lambda address, data: print('IR Received:', address, data))
    while True:
        for i in range(256):
            ir_transmitter.transmit(i, i)
            sleep_ms(100)
except KeyboardInterrupt:
    pass
ir_receiver.set_enable(False)
modules.clear() # make sure we can re-import the example!
print('''
Done!
Can press ctrl-d to soft-reset.
''')
