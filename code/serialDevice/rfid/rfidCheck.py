import serial
import time
tag = ["0900711DDFBA"]

port = serial.Serial("/dev/ttyUSB1", baudrate = 9600, timeout = 2)
while True:
    
    rcv = port.read(12)
    print rcv
    time.sleep(1)
    for i in range(len(tag)):
        if rcv == tag[i]:
            print("welcome ankit mishra")

        else:
            print("not identified")
            print(rcv)
