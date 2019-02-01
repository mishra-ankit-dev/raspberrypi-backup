#!/usr/bin/env python


#import RPi.GPIO as GPIO #Imports RPi for GPIO Use (Comment/Uncomment to use)
import socket # Imports socket function
import struct # Imports structure function
import fcntl # Imports networking function
import time # Imports time function
import os # Imports Operating System function
import re # Imports Reg Ex function
from time import sleep # Imports sleep function from time module
from Documents.code.lcd.lcd2 import *
from Documents.code.lcd.lcd2 import main,lcd_string,lcd_display ,lcd_init


main()
#lcd_display(0x01, LCD_CMD)

# Sends the Temp of the cpu to the lcd display (for 10 seconds)
def tempcpu(): #Defines "tempcpu"
   for _ in range(10): # Sets up timer

        cputemp = os.popen("vcgencmd measure_temp").readline() # Gets temp reading (shows as "temp=xx.x'C")
        celsius = re.sub("[^0123456789\.]", "", cputemp) # Removes everything but numbers and "."
        fahrenheit = int(9.0/5.0*int(float(celsius)+32)) # Math Function Fahrenheit (celsius * 9 / 5 + 32) as interger

        lcd_string("Cpu : {} C".format(celsius), LCD_LINE_1) # Prints Temp as Celsius to the LCD Display line 1
        lcd_string("Temp: {}  F".format(fahrenheit), LCD_LINE_2) # Prints Temp as Fahrenheit to the LCD Display line 2
        sleep(1) # Sleeps for one second before restarting loop
	#lcd_display(0x01, LCD_CMD)

# Sends the Time and Date to the lcd display (for 10 seconds)
def curtime(): # Defines "curtime"
   for _ in range(10): # Sets up timer

        lcd_string("Time: {}".format(time.strftime("%H:%M:%S")), LCD_LINE_1) # Prints time to the LCD Display line 1
        lcd_string("Date: {}".format(time.strftime("%m:%d:%Y")), LCD_LINE_2) # Prints date to the LCD Display line 2

        sleep(1) # Sleeps for one second before restarting loop
	#lcd_display(0x01, LCD_CMD)

# Gets the IP Address
def getaddr(ifname): # Defines "getaddr" as well as ifname arguement later

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24]) # Not sure how this block works just yet, but it does dig up the ip address

# Sends the IP Address to the lcd display (for 10 seconds) as wlan0, eth0 can also be used
def getip(): # Defines "getip"

    ip = getaddr('eth0') # Grabs the address from "eth0" and assigns it to "ip"
    for _ in range(10): # Sets up timer

        lcd_string("IP Address:", LCD_LINE_1) # Prints string to LCD Display line 1
        lcd_string(ip, LCD_LINE_2) # Prints "ip" to LCD Display line 2

        sleep(1) # Sleeps for one second before restarting loop
	#lcd_display(0x01, LCD_CMD)

# runs a forever loop calling the defs above
try: # Gives way to exception later

    #while True: # Forever loop

        tempcpu() # Calls "tempcpu"
        lcd_display(0x01, LCD_CMD) # Clears the LCD Display

        curtime() # Calls "curtime"
        lcd_display(0x01, LCD_CMD) # Clears the LCD Display

        getip() # Calls "getip"
        lcd_display(0x01, LCD_CMD) # Again Clears the LCD Display
        
# Allows for clean exit
except KeyboardInterrupt: # If interrupted by the keyboard ("Control" + "C")
   lcd_display(0x01, LCD_CMD)
   #lcd_display(0x01, LCD_CMD) #clear the lcd display

# Exits the python interperter

finally :
	lcd_display(0x01, LCD_CMD)
	#lcd_display(0x01, LCD_CMD)


