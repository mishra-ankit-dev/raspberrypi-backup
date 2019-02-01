#!/usr/bin/python

import serial
import time

command = ""

# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=26)

# Transmitting AT Commands to the Modem
# '\r' indicates the Enter key

def main():
	gpsdata()


def writegps(command):

	port.write(command + "\r")
	gps_output = port.readline()
	print(gps_output)

def gpsdata():

	port.write('AT+CGPSPWR=1'+'\r')
        rcv = port.readline()
        print rcv

	port.write('AT+CGPSRST=0'+'\r')
        rcv = port.readline()
        print rcv

	while(1):
		port.write('AT+CGPSINF=32'+'\r')
		gps_output = port.readline()
		print gps_output

		#printing humidity and temprature

		#humidity, temperature = Adafruit_DHT.read_retry(11, 4)
		#print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)



if __name__ == '__main__':
	try:
		main()

	except KeyboardInterrupt:
		pass

	finally:
		port.flush()
