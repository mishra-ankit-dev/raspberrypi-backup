#!/usr/bin/python

import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import serial
import os, time

GPIO.setmode(GPIO.BOARD)

# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=26)

# Transmitting AT Commands to the Modem
# '\r' indicates the Enter key

try:

	while(1):
		port.write('AT+CGPSPWR=1'+'\r')
                rcv = port.readline()
                print rcv


		port.write('AT+CGPSRST=0'+'\r')
                rcv = port.readline()
                print rcv

		port.write('AT+CGPSINF=32'+'\r')
		gps_output = port.readline()
		print gps_output

		#printing humidity and temprature

		humidity, temperature = Adafruit_DHT.read_retry(11, 4)
		print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)

except KeyboardInterrupt:
	pass
