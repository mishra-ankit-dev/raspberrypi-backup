#!/usr/bin/env python
# Author : Ankit Mishra
# Date: 30 july, 2018

""" home security system and theft protection using RASPBERRY PI """
# Including some packages
import os
import sys
import time
import serial
import picamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
gateServoPin,alarmPin = 27,18
GPIO.setup(alarmPin, GPIO.OUT)
GPIO.setup(gateServoPin, GPIO.OUT)
GPIO.output(alarmPin, GPIO.HIGH)
GPIO.output(gateServoPin, GPIO.HIGH)


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
        lcd.lcd_string("%s INITIALIZED....." %serialDevice, LCD_LINE_2)
        
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
class myKeypad:

    """ DEFINING SOME GLOBAL VARIABLES """
    global COL
    global ROW
    global MATRIX
    
    ROW = [20,16,12,26]
    COL = [19,13,6,5]
    MATRIX = [
                ['1','2','3','A'],
                ['4','5','6','B'],
                ['7','8','9','C'],
                ['*','0','#','D']
            ]

    """ SETTING PINS OF ROWS AND COLUMN FOR KEYPAD TO BE OUTPUT"""
    for pin in ROW,COL:
        GPIO.setup(pin, GPIO.IN, pull_up_down= GPIO.PUD_UP)

    """ INITIALISES CLASS myKeypad """
    def __init__(self,purpose):
        self.purpose = purpose
        print("keypad object created for %s" % self.purpose)
        lcd.lcd_string("KEYPAD INITIALIZED..", LCD_LINE_3)

    """ READS THE KEY PRESS AND RETURNS THE KEY PRESSED """    
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

class my_lcd:


    global LCD_WIDTH, LCD_CHR, LCD_CMD, LCD_LINE_1, LCD_LINE_2,LCD_LINE_3, LCD_LINE_4,E_PULSE,E_DELAY
    LCD_WIDTH, LCD_CHR, LCD_CMD,LCD_LINE_1, LCD_LINE_2,LCD_LINE_3, LCD_LINE_4, E_PULSE, E_DELAY = 20, True, False,0x80 ,0xC0,0x94,0xD4,0.0005,0.0005

    def __init__(self, pin_rs, pin_e, pins_db):
        
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db

        
        GPIO.setup(self.pin_e, GPIO.OUT)  
        GPIO.setup(self.pin_rs, GPIO.OUT)  
        for pin in self.pins_db:  
            GPIO.setup(pin, GPIO.OUT)  
        self.lcd_init()
        self.lcd_clear()

    
    def lcd_init(self):
        global command
        
        command=[0x33,0x32,0x06,0x0C,0x01]
        for i in range(len(command)):
            self.lcd_byte(command[i], LCD_CMD)
        
        time.sleep(E_DELAY)
        self.lcd_string("LCD INITIALIZED....", LCD_LINE_1)
        time.sleep(1)

    def lcd_clear(self):

        self.lcd_byte(0x01, LCD_CMD)

    def lcd_byte(self,bits,mode):
        """ Send command to LCD """  
  
        time.sleep(0.0005)  
        bits=bin(bits)[2:].zfill(8)          
        GPIO.output(self.pin_rs, mode)  
  
        for pin in self.pins_db:  
            GPIO.output(pin, False)  
  
        for i in range(4):  
            if bits[i] == "1":  
                GPIO.output(self.pins_db[::-1][i], True)  
  
        self.lcd_toggle_enable()
        
        for pin in self.pins_db:  
            GPIO.output(pin, False)  
  
        for i in range(4,8):  
            if bits[i] == "1":  
                GPIO.output(self.pins_db[::-1][i-4], True)  

        self.lcd_toggle_enable()
  
        
    def lcd_toggle_enable(self):
        # Toggle enable
        time.sleep(E_DELAY)
        GPIO.output(self.pin_e, True)
        time.sleep(E_PULSE)
        GPIO.output(self.pin_e, False)
        time.sleep(E_DELAY)

    def lcd_string(self,message,line):
        # Send string to display
         
        message = message.ljust(LCD_WIDTH," ")
         
        self.lcd_byte(line, LCD_CMD)
         
        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]),LCD_CHR)

class cam:
    
    def __init__(self,purpose):
        global camera
        self.purpose = purpose
        camera = picamera.PiCamera()        
        camera.rotation = 180
        print("camera initialization for security")
        lcd.lcd_string("CAMERA INITIALIZED..", LCD_LINE_4)
        

    def image(self, location):

        camera.start_preview()
        time.sleep(2) # hang for preview for 5 seconds
        camera.capture(location)
        camera.stop_preview()
        print("image captured at %s" %location)

    def video(self, name, time, location):
        camera.start_preview()
        camera.start_recording('/home/pi/video.h264')
        time.sleep(10)
        camera.stop_recording()
        camera.stop_preview()
        print("video captured at %s" %location)

    def stop(self):
                
        camera.close()
        
    


# DEFINES THE MAIN PROGRAM WHICH COMPARES PIN ENTERED WITH THE REGISTERED PIN 
def lock():
    
    check = True
    PIN =[]
    lcd.lcd_string("Enter pin to", LCD_LINE_3)
    lcd.lcd_string("open the gate", LCD_LINE_4)
    
    while check:

        """ CHECK FOR THE KEYPRESS TILL KEYBOARDINTERRUPT OR check = False"""
        key = 0
        key = sec.keypad()
        if key:

            """ IF ANY KEY IS PRESSED INTER THIS LOOP(key >0) """
            if key == '#':

                """ IF # IS PRESSED ENTER HERE AND CHECK WHETHER PIN IS CORRECT"""
                pin =0
                pin= ''.join(PIN)
                if pin == "1234":

                    """ ENTER HERE IF THE PIN IS CORRECT """                    
                    GPIO.output(gateServoPin, GPIO.LOW)
                    time.sleep(3)
                    GPIO.output(gateServoPin, GPIO.HIGH)
                    print("OPENING THE GATE")
                    lcd.lcd_string("PUSH GATE TO OPEN", LCD_LINE_1)
                    time.sleep(2)                    
                    lcd.lcd_clear()
                    check = False

                elif pin == "4321":

                    """ IF THE PIN ENTERED IS REVERSE OF REGISTERD PIN, CALL POLICE """
                    lcd.lcd_string("WAIT CHECKING PIN...", LCD_LINE_1)
                    myCam.image('/home/pi/Documents/cam/image.jpg')
                    calling.call("9713490290")
                    GPIO.output(gateServoPin, GPIO.LOW)
                    time.sleep(3)
                    GPIO.output(gateServoPin, GPIO.HIGH)
                    lcd.lcd_string("PUSH GATE TO OPEN", LCD_LINE_1)
                    time.sleep(2)
                    lcd.lcd_clear()
                    check = False
                    
                else:
                    
                    """ IF PIN IS INCORRECT CALL THE HOUSE OWNER """
                    lcd.lcd_string("wrong pin try again!", LCD_LINE_1)                    
                    GPIO.output(alarmPin, GPIO.LOW)
                    myCam.image('~/Documents/cam/image.jpg')
                    calling.call("9713490290")
                    GPIO.output(alarmPin, GPIO.HIGH)
                    lcd.lcd_clear()
                    check = False
                    
            else:

                """ ADD KEYS PRESSED TO PIN AND DISPLAY ON LCD """
                PIN+=key
                lcd.lcd_byte(ord(key),LCD_CHR)
                time.sleep(0.5)
                print("PIN is %s" % "".join(PIN))



if __name__ == '__main__':
    try:
        """ FIRSTLY INITIALISE LCD AND THEN CREATE OBJECTS AND CALL MAIN[lock()] FUNCTION """
        
        lcd = my_lcd(22,11,[23,10,9,25])
        
        calling = write_serial_device("GSM")
        sec = myKeypad("security")
        myCam = cam("security")
        
        time.sleep(2)
        lcd.lcd_clear()
        while 1:
            lock()
    except KeyboardInterrupt:
        print("exiting the program")
        lcd.lcd_string("GOODBYE !!!", LCD_LINE_1)
        time.sleep(2)

    finally:
        lcd.lcd_clear()
        myCam.stop()
        GPIO.cleanup()
