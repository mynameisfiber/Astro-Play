import serial
import dbm
from collections import OrderedDict
import json
import requests
import winsound
Freq = 2500 # Set Frequency To 2500 Hertz
Dur = 250 # Set Duration To 1000 ms == 1 second
winsound.Beep(Freq,Dur)
winsound.Beep(Freq,Dur)

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
pline=0
while True:
    #line = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
    line = arduino.readline().strip()
    #print(line)
    
    cline=line[377:378]
    send=line[382:383]
    if cline==b'':
        cline=pline
    if pline != cline:
        if cline==b'1':
            winsound.Beep(1500,400)
        elif cline==b'2':
            winsound.Beep(1000,300)
        elif cline==b'3':
            winsound.Beep(750,250)
        elif cline==b'':
            winsound.Beep(3500,0)
    pline=cline
    if send==b'1' and cline==b'1':
        winsound.Beep(1200,250)
        winsound.Beep(1500,100)
    if send==b'1' and cline==b'2':
        winsound.Beep(1200,250)
        winsound.Beep(1500,100)
        winsound.Beep(1500,100)
    if send==b'1' and cline==b'3':
        winsound.Beep(1200,250)
        winsound.Beep(1500,100)
        winsound.Beep(1500,100)
        winsound.Beep(1500,100)
        
    print(pline,send)
    if len(line) == 388: #Somtimes a single comes through the Serial port
        newstring = line.decode(encoding='UTF-8')
        #print(type(newstring))
        #print(newstring) #check to see if converted to a string
        
        for item in newstring.split(','): # break apart JSON string into key and value
           item = item.strip()  #First grab individual key value pairs
           #print(type(item))  #check to see if string
           #print("Item=",item)
           key, value = (item.split(':')) # split the pairs into key and Value
           #print(type(key)," key ",key, type(value)," value ",value)
           value = int(value.strip()) #make value an integer
           key = int(key.strip()) #needed to match the existing int inside data-dict
           #print(type(value)," ",value)
           data[key] = value #assign resistor value to its position in the string 
           #print(type(key),key, type(data[key])," ",data[key])
           #print(data.items())  ## A Ha two versions of the dict!
        for x in data.keys(): # Look up Token value. Account for resistor slop with a range. Assign to new dict named Tokens
          if 200 <= data[x] <=212:#f forward
             strdec=db.get("208",0)  
             Tokens[x]=strdec.decode(encoding='UTF-8')
          elif 900 <= data[x] <=917:
              strdec=db.get("912",0) #r right
              Tokens[x]=strdec.decode(encoding='UTF-8')
          elif 890 <= data[x] <=899:
              strdec=db.get("895",0) # 45 degrees
              Tokens[x]=strdec.decode(encoding='UTF-8')
          elif 989 <= data[x] <=999:
              strdec=db.get("991",0) #10 numeric
              Tokens[x]=strdec.decode(encoding='UTF-8')
          elif 550 <= data[x] <=559:
              strdec=db.get("556",0) #90 degrees
              Tokens[x]=strdec.decode(encoding='UTF-8')
          elif 1020 <= data[x] <=1024:
              Tokens[x]= ""      #Blank
        sortkeys = OrderedDict(sorted(Tokens.items()))
        print(sortkeys)
        #with open('dict-json.txt','w') as outfile:
         #   json.dump(Tokens,outfile)
        if send == b'1':
            print("Sending JSON")
            data_json = json.dumps(Tokens)
            #print(type(data_json))
            #print(data_json)
            #payload = {'json_playload': data_json }
            r = requests.post('http://10.2.108.1:9999',data=data_json)
            print("Done sending")

		
