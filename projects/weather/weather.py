# Author: Ankit Mishra
# Date: 09 Sep, 2018
# Title: IOT based Real time weather detection and pridiction

""" 
"""


#!/usr/bin/python

import os
import sys
import math
import time
import glob
import serial
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix

#reload(sys)
#sys.setdefaultencoding('utf8')
class serial_device():
    
    def __init__(self):
        """ Initializes the class iobject """

        #self.port = serial.Serial("/dev/ttyUSB0", baudrate = 9600, timeout = 2)
        print("serial_device object created")
        port_detect = glob.glob("/dev/ttyUSB*")
        print(len(port_detect),"Ports detected")
        if (len(port_detect) != 0):				
            print("Ports detected is/are:")
            for i in range (0,len(port_detect)):
                print(port_detect[i])
            if (len(port_detect) == 1):
                self.port = serial.Serial(port_detect[0],baudrate=9600)
                print("connected to: {}".format(port_detect[0]))

            else:
                for i in range(0,len(port_detect)):
                    print("Enter",i,"to connect to:",port_detect[i])
                    y = int(input("Enter your choice of connection: "))
                    while (y >= len(port_detect)):
                        print("Invalid choice")
                        for i in range(0,len(port_detect)):
                            print('Enter {} to select: {}'.format(i, detect_port[i]))
                        y = int(input('Enter your choice of connection'))
                    self.port = serial.Serial(port_detect[y], baudrate=9600)
                    print('Connected to: {}'.format(port_detect[y]))
                    #return

            

    def write_gps(self,*commands):
        """ Writes commands to the serial port """

        rcv = ""
        self.port.write(*commands)
        rcv = self.port.readline()
        print(rcv)
        return rcv
    
class extract(serial_device):

    def __init__(self):
        self.timestring = dt.datetime.now()
        print("Extract object created at {}".format(self.timestring))
        
    def log_file(self):
        """ Saves the sensor datas to the file """

        global gps_data,gps_output
        
        dev.write_gps('AT+CGPSPWR=1')
        dev.write_gps('AT+CGPSRST=0')
        self.timestring = dt.datetime.now()
        gps_output = dev.write_gps('AT+CGPSINF=32').split(',')
        temp = ['42','88']
        gps_output = gps_output[:9]+temp
        #temperature,humidity = Adafruit.read_retry(11,7)
        gps_data = pd.read_csv('in.csv', encoding = 'utf8')
        #gps_output = gps_data.ix[1,:]
        gps_data = gps_data.ix[:,['nmea','time','valid','lat','lat_direction','lon','lon_direction','speed','date','temp','Humidity']]
        if (gps_output[0]=='$GPRMC') & (gps_output[2] == 'A'):
            print(gps_output)
            gps_data.ix[len(gps_data.nmea)+1,:] = gps_output
            gps_data.fillna(-99999,inplace = False)
            gps_data.to_csv('in.csv',index = True)
            print(gps_data.tail(3))

    def out_file(self):
        """ Outputs a file which contains inmportant data """

        if (gps_output[0]=='$GPRMC') & (gps_output[2] == 'A'):
            data = pd.read_csv('out.csv')
            data = data[gps_data.ix[:, 'nmea'] == '$GPRMC'].ix[:len(gps_data.nmea)-1, ['lat','lon','speed','temp','Humidity','datetime']]
            data.datetime = pd.to_datetime(data.datetime, infer_datetime_format=True)
            data.ix[len(gps_data.nmea)-1, 'speed'] = round((gps_data.speed.get_values().tolist()[0]) * 1.852, 0)
            #print((data.lat.get_values().tolist()[0]))
            data.ix[len(gps_data.nmea)-1,'lat'] = round(((gps_data.lat.get_values().tolist()[0]) / 100) + ((data.lat.get_values().tolist()[0]) % 100) / 60, 6)
            data.ix[len(gps_data.nmea)-1,'lon'] = round(((gps_data.lon.get_values().tolist()[0]) / 100) + ((data.lon.get_values().tolist()[0]) % 100) / 60, 6)
            data.ix[len(gps_data.nmea)-1, 'datetime'] = self.timestring
            if gps_data.ix[len(gps_data.nmea),'lat_direction'] == 'S':
                data.ix[len(gps_data.nmea)-1, 'lat'] =  float(data.ix[len(gps_data.nmea)-1, 'lat']) * -1
                pass
            if gps_data.ix[len(gps_data.nmea),'lon_direction'] == 'W':
                data.ix[len(gps_data.nmea)-1, 'lon'] =  float(data.ix[len(gps_data.nmea)-1, 'lon']) * -1
                pass
            else:
                pass
                print(data.tail())
        
            data.to_csv('out.csv',index= True)

class plot_graph():

    def __init__(self):
        """ This function initiatizes the plot_graph class """
        print("The object for plotting graph is created")

    def plot_temp_humid(self):
        data = pd.read_csv('out.csv')
        data.plot(kind = 'scatter', y ='speed', x ='temp', color = 'red')
        #data.speed.astype='float64'
        grouped = data[['speed','temp']]
        #print (grouped)
        scatter_matrix(grouped, alpha = 0.2, figsize=(70, 70))
        plt.show()
        
grf = plot_graph()
dev = serial_device()
ser = extract()
def main():
    grf.plot_temp_humid()
    while True:
        ser.log_file()
        ser.out_file()
        time.sleep(2)
if __name__ == '__main__':
    try:
        main()
#    except ValueError:
#        pass
    except KeyboardInterrupt:
        pass
