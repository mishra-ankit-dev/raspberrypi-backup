#!/usr/bin/env python
# Author : Ankit Mishra
# Date: 30 july, 2018

""" home security system and theft protection using RASPBERRY PI """
# Including some packages
import os
import sys
import time
import serial
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sys.path.append('/home/pi/Documents/lcd')
from lcd import *

# defining class for serial devices(GSM OR GPS)
class write_serial_device:
    global port
    global rcv
    rcv = ""
    
    def __init__(self, serialDevice):

        """INITIALIZES THE CLASS AND SERIAL PORT(whether gsm or gps) WHEN OBJECT IS CREATED"""
        self.serialDevice = serialDevice
        print("connecting to %s" %self.serialDevice)

        if self.serialDevice == "GSM":
            self.port = serial.Serial("/dev/ttyUSB0", baudrate = 9600, timeout = 20)
        elif self.serialDevice == "gps":
            self.port = serial.Serial("/dev/ttyUSB1", baudrate = 9600, timeout = 20)

    def write_port(self, command, readByte, sleepTime):

        """ WRITES COMMAND TO THE ABOVE SELECTED PORT """
        self.port.write(command+"\r")
        rcv = self.port.read(readByte)
        print (rcv)
        time.sleep(sleepTime)
        #print ("working")

    def call(self, mobNum):
        
        """ PLACES A CALL TO A SPECIFIED NO PASSED IN THE ARGUMENT """
        self.write_port("ATD+91%s;" %mobNum ,20,15)

    def send_msg(self, mobNum, message):

        """ SENDS THE MESSAGE TO THE SPECIFIED NO. AS PER THE ARGUMENT PASSED"""
        command = "AT+CGMS"+ mobNum
        self.write_port(command, 10, 1)
        self.write_port("message",10,2)

# CREATING CLASS FOR KEYPAD
class keyp:

    global COL
    global ROW
    global MATRIX

    MATRIX = [
                ['1','2','3','A'],
                ['4','5','6','B'],
                ['7','8','9','C'],
                ['*','0','#','D']
            ]

    ROW = [20,16,12,26]
    COL = [19,13,6,5]
    for pin in ROW,COL:
        GPIO.setup(pin, GPIO.IN, pull_up_down= GPIO.PUD_UP)

    def __init__(self,purpose):
        self.purpose = purpose
        print("keypad object created for %s" % self.purpose)
        
    def keypad(self):
        for j in range(4):
            GPIO.setup(COL[j], GPIO.OUT)
            GPIO.output(COL[j], 0)
            ch=0
            for i in range(4):
                if GPIO.input(ROW[i])==0:
                    ch=MATRIX[i][j]
             
                    print( "Key Pressed is %s:" %ch)
                    time.sleep(0.25)
                    return ch
                    while (GPIO.input(ROW[i]) == 0):
                        pass
            GPIO.output(COL[j],1)

  
gateServoPin,alarmPin = 27,18
GPIO.setup(alarmPin, GPIO.OUT)
GPIO.setup(gateServoPin, GPIO.OUT)
GPIO.output(alarmPin, GPIO.HIGH)
GPIO.output(gateServoPin, GPIO.LOW)


def lock():
    PIN =[]
    while True:
        
        key = 0
        key = sec.keypad()
        if key >0:
            
            if key == '#':
                pin =0
                pin= ''.join(PIN)
                if pin == "1234":

                    GPIO.output(gateServoPin, GPIO.HIGH)
                    print("OPENING THE GATE")
                    lcd_string("PUSH THE GATE TO OPEN", LCD_LINE_1)
                    time.sleep(2)
                    lcd_clear()
                    PIN = []
                    lcd_string("Enter pin to", LCD_LINE_3)
                    lcd_string("open the gate", LCD_LINE_4)
                    
                elif pin == "4321":
                    print "working"
                    PIN = []
                    lcd_clear()
                    lcd_string("Enter pin to", LCD_LINE_3)
                    lcd_string("open the gate", LCD_LINE_4)
                    calling.call("9713490290")
                    
                else:
                    lcd_string("wrong pin try again!", LCD_LINE_1)
                    time.sleep(2)
                    lcd_clear()
                    PIN = []
                    lcd_string("Enter pin to", LCD_LINE_3)
                    lcd_string("open the gate", LCD_LINE_4)
                    GPIO.output(alarmPin, GPIO.LOW)
                    calling.call("9713490290")
                    GPIO.output(alarmPin, GPIO.HIGH)
                    
            else:
                PIN+=key
                lcd_byte(ord(key),True)
                time.sleep(0.5)
                print("PIN is %s" % "".join(PIN))



if __name__ == '__main__':
    try:
        main()
        lcd_clear()
        calling = write_serial_device("GSM")
        sec = keyp("security")

        lcd_string("GSM CONNECTED", LCD_LINE_1)
        lcd_string("KEYPAD CONNECTED", LCD_LINE_2)
        time.sleep(2)
        lcd_clear()
        lcd_string("Enter pin to", LCD_LINE_3)
        lcd_string("open the gate", LCD_LINE_4)
        lock()
    except KeyboardInterrupt:
        print("exiting the program")

    finally:
        lcd_clear()
        GPIO.cleanup()
