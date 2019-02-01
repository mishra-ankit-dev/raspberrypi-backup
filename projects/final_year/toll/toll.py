#!usr/bin/python

# Date : 14 Aug,2018
# Author : Ankit Mishra
# contact me on amishm766@gmail.com

""" IOT based toll collection with RFID using Raspberry pi """

import os
import csv
import sys
import time
import serial
import sqlite3
import datetime

global bal, min_balance
min_balance = 30
output_file = "customer.csv"
input_file = "change.csv"

class csv_class:

    def __init__(self):
        print("creating csv object")

    def column(self, filename):
        arr = []
        codes = []
        names = []
        balance = []        
        with open(filename) as f:            
            for row in f:
                arr=row.split(',')
                codes.append(arr[1])
                names.append(arr[0])
                balance.append(arr[2])
            return names, codes, balance

    def csv_write(self, filename, mode, column1, column2, column3):
        text = [column1, column2, column3]
        with open(filename, mode) as f: 
            writer = csv.writer(f, delimiter = ",", lineterminator ='\n')
            writer.writerow(text)

    def csv_read_column(self, filename, columnNo):
        col = []        
        with open(filename, 'rb') as infile:
            for row in infile:
                arr = row.split(",")
                col.append(arr[columnNo - 1])
            return col                                    
                    

class serial_device():
    global port
    if os.path.exists("/dev/ttyUSB0"):
        port = serial.Serial("/dev/ttyUSB0", baudrate = 9600, timeout = 2)    

    def __init__(self, purpose, device):
        self.purpose = purpose
        self.device = device
        print("{} is initialized for {}".format(self.device, self.purpose))

    def serial_read(self):
        rcv = port.read(12)
        time.sleep(0.25)
        return rcv

class check():
    def __init__(self):
        print("checking the database")

    def check_balance(self):
        names, codes, balance = col.column(input_file)
        #code = 'B'
        for i in range(len(codes)):
            if code == codes[i]:
                print("your balance is {}".format(balance[i]))
        return balance[i]

    def deduct_balance(self):        
        names, codes, balance = col.column(input_file)
        #code = 'B'
        for i in range(len(codes)):
            if code == codes[i]:
                tax = 20
                #print("your balance is {}".format(balance[i]))
                balance[i] = str(int(balance[i])-tax) + '\n'
                print("Rs. {} has been deducted from your account".format(tax))
                print ("the new balance is {}".format(balance[i]))
                col.csv_write(input_file, "w", "name", "tag", "balance")
                for j in range(1,len(codes)):
                    col.csv_write(input_file, "a", names[j], codes[j], balance[j][:-1])            

    def check_database(self):
        time_string = datetime.datetime.now()
        names, codes, balance = col.column(input_file)
        #code = 'B'
        for i in range(len(codes)):
            if code == codes[i]:                
                #col.csv_write(output_file, "w", "name", "tag", "crossing time")
                col.csv_write(output_file, "a", names[i], codes[i], time_string)
                print("hello {}".format(names[i]))
                value = 'True'
                return value
            else:
                pass
                #print("Match not found")

def main():
    global col, code
    rfid = serial_device('security','rfid')
    col = csv_class()
    sec = check()
    while True:
        code = rfid.serial_read()
        if sec.check_database() == 'True':
            current_balance = int(sec.check_balance()) 
            if current_balance > min_balance:               
                sec.deduct_balance()
                time.sleep(0.5)
            else:
                print("insufficient fund")
        else:
            print("Swipe the card")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
