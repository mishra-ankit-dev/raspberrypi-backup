import lcd
import time
import RPi.GPIO as GPIO
D4=31
D5=33
D6=35
D7=37
RS=7
EN=29
mylcd=lcd.lcd()
print("hii")
mylcd.begin(D4,D5,D6,D7,RS,EN)
mylcd.Print("How are you")
time.sleep(2)
mylcd.clear()
mylcd.Print("I am RaspberryPi") 
mylcd.setCursor(2,1)
mylcd.Print("Electro-Passion")
time.sleep(2)
mylcd.clear()
mylcd.Print("Seconds=")
seconds=0
mylcd.setCursor(1,9)
mylcd.Print(seconds)
mylcd.shift(mylcd.right,5)
mylcd.shift(mylcd.left,5)
mylcd.blinkCursorOn()
time.sleep(2)
mylcd.blinkCursorOff()
