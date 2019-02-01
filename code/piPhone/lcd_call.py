#!usr/bin/env python
import serial
import time
import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/Documents/lcd')
from lcd import *
sys.path.append('/home/pi/Documents/gsm')
from gsm import *

#port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=100)


main()
write("ATD9713490290;")
#port.write('ATD9713490290;'+'\r')
#rcv = port.readline()
#print rcv
time.sleep(2)
lcd_string("calling", LCD_LINE_1)
lcd_string("9713490290", LCD_LINE_2)
time.sleep(10)
lcd_byte(0x01, LCD_CMD)

