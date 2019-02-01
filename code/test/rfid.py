import serial
import time

port = serial.Serial('/dev/ttyUSB0', baudrate = 19200, timeout = 2)
check = True
while check:
    port.write('AT')
    #port.write('ATD+919713490290;')
    rcv = port.read(2)
    print rcv
    time.sleep(1)
    #check = False
