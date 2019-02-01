import RPi.GPIO as gpio
import serial
import time

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
ROW = [4,25,24,23]
COL = [26,19,13,6]




gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

while(1):
   for j in range(4):
     gpio.setup(COL[j], gpio.OUT)
     gpio.output(COL[j], 0)
     ch=0
     for i in range(4):
       gpio.setup(ROW[i],gpio.IN, pull_up_down = gpio.PUD_UP)
       if gpio.input(ROW[i])==0:
         ch=MATRIX[i][j]
         #return ch
         print ch
         while (gpio.input(ROW[i]) == 0):
          pass
     gpio.output(COL[j],1)
