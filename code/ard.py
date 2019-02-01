from nanpy import (ArduinoApi, SerialManager)
from time import sleep

ledPin = 13
#groundPin = 2
#highPin = 4
#gasPin = 0

try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
    print('connected to arduino')
except:
    print('failed coneection')

a.pinMode(ledPin, a.OUTPUT)
a.pinMode(gasPin, a.INPUT)

try:
    while(True):
        #a.digitalWrite(groundPin, a.LOW)
        #a.digitalWrite(highPin, a.HIGH)
        print('led')
        a.digitalWrite(ledPin, a.HIGH)
        print("on")
        sleep(1)
        print('led')
        a.digitalWrite(ledPin, a.LOW)
        print('off')
        sleep(1)
        print('starting')
        #out = a.digitalRead(gasPin)
        #print('working...')
        #print(out)
except:
    a.digitalWrite(ledPin, a.LOW)
