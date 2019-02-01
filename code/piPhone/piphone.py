import RPi.GPIO as gpio
import serial
import time

msg=""
#     0      7   11  15  19  23  27   32  36   414244   ROLL45
alpha="1!@.,:?ABC2DEF3GHI4JKL5MNO6PQRS7TUV8WXYZ90 *#"
x=0
y=0

MATRIX = [
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D']
         ]
ROW = [20,16,12,26]
COL = [19,13,6,5]

moNum=['0','0','0','0','0','0','0','0','0','0']

m11=17
m12=27
led=4
buz=1

button=19

RS =22
EN =11
D4 =23
D5 =10
D6 =9
D7 =25

HIGH=1
LOW=0

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(RS, gpio.OUT)
gpio.setup(EN, gpio.OUT)
gpio.setup(D4, gpio.OUT)
gpio.setup(D5, gpio.OUT)
gpio.setup(D6, gpio.OUT)
gpio.setup(D7, gpio.OUT)
gpio.setup(led, gpio.OUT)
gpio.setup(buz, gpio.OUT)
gpio.setup(m11, gpio.OUT)
gpio.setup(m12, gpio.OUT)
gpio.setup(button, gpio.IN)
gpio.output(led , 0)
gpio.output(buz , 0)
gpio.output(m11 , 0)
gpio.output(m12 , 0)
for j in range(4):
    gpio.setup(COL[j], gpio.OUT)
    gpio.setup(COL[j],1)
  
for i in range (4):
    gpio.setup(ROW[i],gpio.IN,pull_up_down=gpio.PUD_UP)
Serial = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=2)
data=""

def begin():
  lcdcmd(0x33) 
  lcdcmd(0x32) 
  lcdcmd(0x06)
  lcdcmd(0x0C) 
  lcdcmd(0x28) 
  lcdcmd(0x01) 
  time.sleep(0.0005)
 
def lcdcmd(ch): 
  gpio.output(RS, 0)
  gpio.output(D4, 0)
  gpio.output(D5, 0)
  gpio.output(D6, 0)
  gpio.output(D7, 0)
  if ch&0x10==0x10:
    gpio.output(D4, 1)
  if ch&0x20==0x20:
    gpio.output(D5, 1)
  if ch&0x40==0x40:
    gpio.output(D6, 1)
  if ch&0x80==0x80:
    gpio.output(D7, 1)
  gpio.output(EN, 1)
  time.sleep(0.005)
  gpio.output(EN, 0)

  # Low bits
  gpio.output(D4, 0)
  gpio.output(D5, 0)
  gpio.output(D6, 0)
  gpio.output(D7, 0)
  if ch&0x01==0x01:
    gpio.output(D4, 1)
  if ch&0x02==0x02:
    gpio.output(D5, 1)
  if ch&0x04==0x04:
    gpio.output(D6, 1)
  if ch&0x08==0x08:
    gpio.output(D7, 1)
  gpio.output(EN, 1)
  time.sleep(0.005)
  gpio.output(EN, 0)
  
def lcdwrite(ch): 
  gpio.output(RS, 1)
  gpio.output(D4, 0)
  gpio.output(D5, 0)
  gpio.output(D6, 0)
  gpio.output(D7, 0)
  if ch&0x10==0x10:
    gpio.output(D4, 1)
  if ch&0x20==0x20:
    gpio.output(D5, 1)
  if ch&0x40==0x40:
    gpio.output(D6, 1)
  if ch&0x80==0x80:
    gpio.output(D7, 1)
  gpio.output(EN, 1)
  time.sleep(0.005)
  gpio.output(EN, 0)

  # Low bits
  gpio.output(D4, 0)
  gpio.output(D5, 0)
  gpio.output(D6, 0)
  gpio.output(D7, 0)
  if ch&0x01==0x01:
    gpio.output(D4, 1)
  if ch&0x02==0x02:
    gpio.output(D5, 1)
  if ch&0x04==0x04:
    gpio.output(D6, 1)
  if ch&0x08==0x08:
    gpio.output(D7, 1)
  gpio.output(EN, 1)
  time.sleep(0.005)
  gpio.output(EN, 0)

def lcdclear():
  lcdcmd(0x01)
 
def lcdprint(Str):
  l=0;
  l=len(Str)
  for i in range(l):
    lcdwrite(ord(Str[i]))
def setCursor(x,y):
    if y == 0:
        n=128+x
    elif y == 1:
        n=192+x
    lcdcmd(n)

def keypad():
   for j in range(4):
     gpio.setup(COL[j], gpio.OUT)
     gpio.output(COL[j], 0)
     ch=0
     for i in range(4):
       if gpio.input(ROW[i])==0:
         ch=MATRIX[i][j]
         #lcdwrite(ord(ch))
        # print "Key Pressed:",ch
        # time.sleep(2)
         return ch
         while (gpio.input(ROW[i]) == 0):
           pass
     gpio.output(COL[j],1)
    # callNum[n]=ch
   
def serialEvent():
    data = Serial.read(20)
    #if data != '\0':
    print data
    data=""
    
def gsmInit():
    lcdclear()
    lcdprint("Finding Module");
    time.sleep(1)
    while 1:
        data=""
        Serial.write("AT\r");
        data=Serial.read(10)
        print data
        r=data.find("OK")
        if r>=0:
            break
        time.sleep(0.5)
        
    while 1:
        data=""
        Serial.write("AT+CLIP=1\r");
        data=Serial.read(10)
        print data
        r=data.find("OK")
        if r>=0:
            break
        time.sleep(0.5)
        
    lcdclear()
    lcdprint("Finding Network")
    time.sleep(1)
    while 1:
        data=""
        Serial.flush()
        Serial.write("AT+CPIN?\r");
        data=Serial.read(30)
        print data
        r=data.find("READY")
        if r>=0:
            break
        time.sleep(0.5)
    
    lcdclear()
    lcdprint("Finding Operator")
    time.sleep(1)
    while 1:
        data=""
        Serial.flush()
        Serial.read(20)
        Serial.write("AT+COPS?\r");
        data=Serial.read(40)
        #print data
        r=data.find("+COPS:")
        if r>=0:
            l1=data.find(",\"")+2
            l2=data.find("\"\r")
            operator=data[l1:l2]
            lcdclear()
            lcdprint(operator)
            time.sleep(3)
            print operator
            break;
        time.sleep(0.5)
    Serial.write("AT+CMGF=1\r");
    time.sleep(0.5)
    Serial.write("AT+CNMI=2,2,0,0,0\r");
    time.sleep(0.5)
    Serial.write("AT+CSMP=17,167,0,0\r");
    time.sleep(0.5)

def receiveCall(data):
        inNumber=""
        r=data.find("+CLIP:")
        if r>0:
            inNumber=""
            inNumber=data[r+8:r+21]
            lcdclear()
            lcdprint("incoming")
            setCursor(0,1)
            lcdprint(inNumber)
            time.sleep(1)
            return 1

def receiveSMS(data):
    print data
    r=data.find("\",")
    print r
    
    if r>0:
        if data[r+4] == "\r":
            smsNum=data[r+2:r+4]
        elif data[r+3] == "\r":
            smsNum=data[r+2]
        elif data[r+5] == "\r":
            smsNum=data[r+2:r+5]
        else:
            print "else"
        print smsNum
        if r>0:
            
            lcdclear()
            lcdprint("SMS Received")
            setCursor(0,1)
            lcdprint("Press Button B")
            print "AT+CMGR="+smsNum+"\r"
            time.sleep(2)
            return str(smsNum)
    else:
        return 0

def attendCall():
    print "Attend call"
    Serial.write("ATA\r")
    data=""
    data=Serial.read(10)
    l=data.find("OK")
    if l>=0:
        lcdclear()
        lcdprint("Call attended")
        time.sleep(2)
        flag=-1;
        while flag<0:
            data=Serial.read(12);
            print data
            flag=data.find("NO CARRIER")
            #flag=data.find("BUSY")
            print flag
        lcdclear()
        lcdprint("Call Ended")
        time.sleep(1)
        lcdclear()

def readSMS(index):
                print index
                Serial.write("AT+CMGR="+index+"\r")
                data=""
                data=Serial.read(200)
                print data
                r=data.find("OK")
                if r>=0:
                    r1=data.find("\"\r\n")
                    msg=""
                    msg=data[r1+3:r-4]
                    lcdclear()
                    lcdprint(msg)
                    print msg
                    time.sleep(5)
                    lcdclear();
                    smsFlag=0
                    print "Receive SMS"

def getChar(Key, ind, maxInd):
            ch=0
            ch=ind
            lcdcmd(0x0e)
            Char=''
            count=0
            global msg
            global x
            global y
            while count<20:
                key=keypad()
                print key
                if key== Key:
                    setCursor(x,y)
                    Char=alpha[ch]
                    lcdwrite(ord(Char))
                    ch=ch+1
                    if ch>maxInd:
                        ch=ind
                    count=0
                count=count+1
                time.sleep(0.1)
            msg+=Char
            x=x+1
            if x>15:
                x=0
                y=1
            lcdcmd(0x0f)
      
def alphaKeypad():
    lcdclear()
    setCursor(x,y)
    lcdcmd(0x0f)
    msg=""
    while 1:
        key=0
        count=0
        key=keypad()
        if key == '1':
            print key
            ind=0
            maxInd=6
            Key='1'
            getChar(Key, ind, maxInd)
            
        elif key == '2':
            ind=7
            maxInd=10
            Key='2'
            getChar(Key, ind, maxInd)
            
        elif key == '3':
            ind=11
            maxInd=14
            Key='3'
            getChar(Key, ind, maxInd)
            
        elif key == '4':
            ind=15
            maxInd=18
            Key='4'
            getChar(Key, ind, maxInd)

        elif key == '5':
            ind=19
            maxInd=22
            Key='5'
            getChar(Key, ind, maxInd)

        elif key == '6':
            ind=23
            maxInd=26
            Key='6'
            getChar(Key, ind, maxInd)

        elif key == '7':
            ind=27
            maxInd=31
            Key='7'
            getChar(Key, ind, maxInd)

        elif key == '8':
            ind=32
            maxInd=35
            Key='8'
            getChar(Key, ind, maxInd)

        elif key == '9':
            ind=36
            maxInd=40
            Key='9'
            getChar(Key, ind, maxInd)

        elif key == '0':
            ind=41
            maxInd=42
            Key='0'
            getChar(Key, ind, maxInd)

        elif key == '*':
            ind=43
            maxInd=43
            Key='*'
            getChar(Key, ind, maxInd)

        elif key == '#':
            ind=44
            maxInd=44
            Key='#'
            getChar(Key, ind, maxInd)

        elif key== 'D':
            return

def sendSMS():
    print"Sending sms"
    lcdclear()
    lcdprint("Enter Number:")
    setCursor(0,1)
    time.sleep(2)
    moNum=""
    while 1:
        key=0;
        key=keypad()
        #print key
        if key>0:
            if key == 'A'  or key== 'B' or key== 'C':
                print key
                return
            elif key == 'D':
                print key
                print moNum
                Serial.write("AT+CMGF=1\r")
                time.sleep(1)
                Serial.write("AT+CMGS=\"+91"+moNum+"\"\r")
                time.sleep(2)
                data=""
                data=Serial.read(60)
                print data
                alphaKeypad()
                print msg
                lcdclear()
                lcdprint("Sending.....")
                Serial.write(msg)
                time.sleep(1)
                Serial.write("\x1A")
                while 1:
                    data=""
                    data=Serial.read(40)
                    print data
                    l=data.find("+CMGS:")
                    if l>=0:
                        lcdclear()
                        lcdprint("SMS Sent.")
                        time.sleep(2)
                        return;
  
                    l=data.find("Error")
                    if l>=0:
                        lcdclear()
                        lcdprint("Error")
                        time.sleep(1)
                        return
            else:
                print key
                moNum+=key
                lcdwrite(ord(key))
                time.sleep(0.5)

def call():
    print "Call"
    n=0
    moNum=""
    lcdclear()
    lcdprint("Enter Number:")
    setCursor(0,1)
    time.sleep(2)
    while 1:
        key=0;
        key=keypad()
        #print key
        if key>0:
            if key == 'A'  or key== 'B' or key== 'D':
                print key
                return
            elif key == 'C':
                print key
                print moNum
                Serial.write("ATD+91"+moNum+";\r")
                data=""
                time.sleep(2)
                data=Serial.read(30)
                l=data.find("OK")
                if l>=0:
                    lcdclear()
                    lcdprint("Calling.....")
                    setCursor(0,1)
                    lcdprint("+91"+moNum)
                    time.sleep(30)
                    lcdclear()
                    return
                #l=data.find("Error")
                #if l>=0:
                else:
                    lcdclear()
                    lcdprint("Error")
                    time.sleep(1)
                    return
            else:
                print key
                moNum+=key
                lcdwrite(ord(key))
                n=n+1
                time.sleep(0.5)
#def main():
begin()
lcdcmd(0x01)
lcdprint("  Mobile Phone  ")
lcdcmd(0xc0)
lcdprint("    Using RPI     ")
time.sleep(3)
lcdcmd(0x01)
lcdprint("Ankit Mishra")
lcdcmd(0xc0)
lcdprint("Welcomes you")
time.sleep(3)
gsmInit()
smsFlag=0
index=""

while 1:

    key=0
    key=keypad()
    print key
    if key == 'A':
      attendCall()
    elif key == 'B':
      readSMS(index)
      smsFlag=0
    elif key == 'C':
      call()
    elif key == 'D':
      sendSMS()
      
    data=""
    Serial.flush()
    data=Serial.read(150)
    print data
    l=data.find("RING")
    if l>=0:
      callstr=data
      receiveCall(data)
    l=data.find("\"SM\"")
    if l>=0:
      smsstr=data
      smsIndex=""
      (smsIndex)=receiveSMS(smsstr)
      print smsIndex
      if smsIndex>0:
          smsFlag=1
          index=smsIndex
    if smsFlag == 1:
        lcdclear()
        lcdprint("New Message")
        time.sleep(1)

    setCursor(0,0)
    lcdprint("C--> Call <--A");
    setCursor(0,1);
    lcdprint("D--> SMS  <--B")
