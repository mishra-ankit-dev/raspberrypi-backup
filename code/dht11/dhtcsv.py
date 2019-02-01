#!/usr/bin/python


from datetime import datetime
import csv
import os
import sys
import Adafruit_DHT
import time

try:
	filename = "/var/www/html/dht_log.csv"
	write_header = not os.path.exists(filename) or os.stat(filename).st_size == 0


	with open(filename, "a") as f_output:
    		csv_output = csv.writer(f_output)

    		if write_header:
        		csv_output.writerow(["Time", "Temperature", "Humidity"])

    		while True:
			humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    			print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)

        		row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), temperature , humidity]
        		csv_output.writerow(row)
	        	time.sleep(5)
except KeyboardInterrupt:
	pass
