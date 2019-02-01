import Adafruit_DHT
import time
import csv
import sys
csvfile = "/home/pi/Documents/samsung/temp.csv"
als = True
while als: 
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4) # gpio pin 4 or pin number 7
    if humidity is not None and temperature is not None:
      humidity = round(humidity, 2)
      temperature = round(temperature, 2)
      print 'Temperature = {0:0.1f}*C  Humidity = {1:0.1f}%'.format(temperature, humidity)
    else:
      print 'can not connect to the sensor!'
    timeC = time.strftime("%I")+':' +time.strftime("%M")+':'+time.strftime("%S")
    data = [temperature, timeC]

    with open(csvfile, "a")as output:
        writer = csv.writer(output, delimiter=",", lineterminator = '\n')
        writer.writerow(data)
    time.sleep(.1) # update script every 60 seconds
