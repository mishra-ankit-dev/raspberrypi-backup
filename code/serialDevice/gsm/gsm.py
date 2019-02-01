#!/usr/bin/env python
import time
import serial
import sys
import RPi.GPIO as GPIO


command = ""

#Define port for serial communication
port = serial.Serial("/dev/ttyUSB0", baudrate = 9600, timeout = 20)

#define main function
#def main():
	#atcommand = raw_input("which AT command you want to write?")
	#write("ATD9713490290;")

def writeAT():
	write("AT")

#define function to write AT commands
def write(command):

	#print("running")
	port.write(command + "\r")
	rcv = port.readline()
	print (rcv)
	#print ("plz... wait")
	#time.sleep(1)



if __name__ == '__main__' :
	try:
		main()

	except KeyboardInterrupt:
		pass

	except IOError:
		print("could not connect")
		print ("exiting")
	except (RuntimeError, TypeError, NameError):
		pass

	except:
		print("unexpectederror")

	finally :
		port.flush()
