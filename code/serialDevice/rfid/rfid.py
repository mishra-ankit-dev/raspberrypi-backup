import serial
import time

port = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout = 1)

while True:
    rcv = port.read(12)
    print rcv
    time.sleep(0.5)
