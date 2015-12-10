import serial
import dbm
from collections import OrderedDict

# open a DB. The c option opens in read/write mode and creates the file if needed.
db = dbm.open('resistorvalues', 'c')
# initialize a dict of keys and values
data = dict.fromkeys([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50])
         # values initially set to None
#print(data.items()) 
Tokens = dict.fromkeys([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50])
        # values initially set to None
#print(Tokens.items())
# Define serial object on COM5 baud 115200
#arduino = serial.Serial('COM5', 115200, timeout=.1)
arduino = serial.Serial('COM9', 57600, timeout=.1)
while True:
    #line = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
    line = arduino.readline().strip()
    #print(line)
    if len(line) == 388: #Somtimes a single comes through the Serial port
        newstring = line.decode(encoding='UTF-8')
        #print(type(newstring))
        #print(newstring) #check to see if converted to a string
        bigdict ={}
        #print(type(bigdict))
        for item in newstring.split(','):
           item = item.strip()
           #print(type(item))  #check to see if string
           #print("Item=",item)
           key, value = (item.split(':'))
           #print(type(key)," key ",key, type(value)," value ",value)
           value = int(value.strip())
           key = int(key.strip()) #needed to match the existing int inside data-dict
           #print(type(value)," ",value)
           data[key] = value
           #print(type(key),key, type(data[key])," ",data[key])
           #print(data.items())  ## A Ha two versions of the dict!
        for x in data.keys():
          if 200 <= data[x] <=212:
             #print(data[x])
             #print(db.get("208",0))
             Tokens[x]=db.get("208",0) #f forward
             #print(Tokens[x])
          elif 900 <= data[x] <=917:
              Tokens[x]=db.get("912",0) #r right
          elif 890 <= data[x] <=899:
              Tokens[x]=db.get("895",0) # 45 degrees
          elif 989 <= data[x] <=999:
              Tokens[x]=db.get("991",0) #10 numeric
          elif 550 <= data[x] <=559:
              Tokens[x]=db.get("556",0) #90 degrees
          elif 1020 <= data[x] <=1024:
              Tokens[x]= ""      #Blank
        sortkeys = OrderedDict(sorted(Tokens.items()))
        print(sortkeys)

		
#Insert dbm lookup of captured serial values
#if db.get(ibutton,0) != 0:
 #        print(str(db.get(ibutton)) + ' is the Command of ' + ibutton)
# else:
 #          print('I do not have command information for ' + ibutton)
  #         print('What is the command')
  #         command = input()
  #         db[ibutton] = command
   #        print('ibutton database updated.')
