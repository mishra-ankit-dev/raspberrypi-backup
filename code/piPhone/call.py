#!/usr/bin/env python

import RPi.GPIO as gpio
import serial
import time
import sys
sys.path.append('/home/pi/Documents/lcd')
from lcd import *
sys.path.append('/home/pi/Documents/gsm')
from gsm import *



rcv = ""
moNum=['0','0','0','0','0','0','0','0','0','0']
msg=""
alpha="1!@.,:?ABC2DEF3GHI4JKL5MNO6PQRS7TUV8WXYZ90 *#"
x=0
y=0

MATRIX = [
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D']
         ]
ROW = [20,16,12,26]
COL = [19,13,6,5]

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)


for j in range(4):
    gpio.setup(COL[j], gpio.OUT)
    gpio.setup(COL[j],1)
  
for i in range (4):
    gpio.setup(ROW[i],gpio.IN,pull_up_down=gpio.PUD_UP)




def keypad():
   for j in range(4):
     gpio.setup(COL[j], gpio.OUT)
     gpio.output(COL[j], 0)
     ch=0
     for i in range(4):
       if gpio.input(ROW[i])==0:
         ch=MATRIX[i][j]
         #lcdwrite(ord(ch))
        # print "Key Pressed:",ch
        # time.sleep(2)
         return ch
         while (gpio.input(ROW[i]) == 0):
           pass
     gpio.output(COL[j],1)
    # callNum[n]=ch

def call():
    print "Call"
    n=0
    moNum=""
    lcd_clear()
    lcd_string("Enter Number:", LCD_LINE_1)
    #setCursor(0,1)
    time.sleep(2)
    while 1:
        key=0;
        key=keypad()
        #print key
        if key>0:
            if key == 'A'  or key== 'B':
                print key
                return
            elif key == 'C':
                print key
                print moNum
                write("ATD+91"+moNum+";\r")
                data=""
                time.sleep(2)
                data=port.read(30)
                l=data.find("OK")
                if l>=0:
                    lcd_clear()
                    lcd_string("Calling.....", LCD_LINE_1)
                    #setCursor(0,1)
                    lcd_string("+91"+moNum, LCD_LINE_2)
		    i = 0
		    #while i<=30:
			#key1 =keypad()
			#if key1== 'D':
				#write("ATH")
				#time.sleep(1)
		        #i=i+1
                    time.sleep(30)
                    lcd_clear()
                    return
                #l=data.find("Error")
                #if l>=0:
                else:
                    lcd_clear()
                    lcd_string("Error", LCD_LINE_1)
                    time.sleep(1)
                    return
            else:
                print key
                moNum+=key
		#print ord(key)
                #lcd_string(ord(key), LCD_LINE_2)
                n=n+1
                time.sleep(0.5)



def main1():
	main()
	lcd_string("A-attend  B-   ", LCD_LINE_1)
	lcd_string("C-call    D-Hold", LCD_LINE_2)
	while True:
		lcd_string("A-attend  B-   ", LCD_LINE_1)
	        lcd_string("C-call    D-Hold", LCD_LINE_2)
		key=0
		key = keypad()
		if key == 'A':
			write("ATA")
		elif key == 'D':
			write("ATH")
		elif key == 'C':
			#write("ATD9981631827;")
			call()

if __name__ == '__main__':
	try:
		main1()

	except KeyboardInterrupt:
		pass

	#except :
		#print("unexpected error")
	finally:
		lcd_clear()
		GPIO.cleanup()
