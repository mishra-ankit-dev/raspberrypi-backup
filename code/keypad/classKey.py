import time
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
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

key = keyp("security")
while True:
    key.keypad()
