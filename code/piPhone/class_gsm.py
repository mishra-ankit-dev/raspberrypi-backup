#/usr/bin/python

import time
import serial

class phone():
	global port
	port = serial.Serial("/dev/ttyUSB0" , baudrate = 9600,timeout =20)
	global rcv
	rcv=""
	def __init__(self,mobNum):
		self.mobNum = mobNum

	def call(self):
		port.write("ATD+91"+ self.mobNum+";\r")
		print ("calling")
		rcv= port.readline()
		print rcv


action = phone("9713490290")
action.call()
time.sleep(5)
