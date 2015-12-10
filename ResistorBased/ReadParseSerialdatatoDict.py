import serial
import dbm
# open a DB. The c option opens in read/write mode and creates the file if needed.
db = dbm.open('ibuttondb', 'c')
# initialize a dict of keys and values
data = dict.fromkeys(  # values initially set to None
         '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50'.split()
         )
# Define serial object on COM5 baud 115200
#arduino = serial.Serial('COM5', 115200, timeout=.1)
arduino = serial.Serial('COM9', 57600, timeout=.1)
while True:
    #line = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
    line = arduino.readline().strip()
    if len(line) == 388:
        newstring = line.decode(encoding='UTF-8')
        #print(newstring)
        for item in newstring.split(','):
         item = item.strip()
        key, value = item.split(':')
        value = int(value)
        data[key] = value
        print(data.keys())
    
  


		
#Insert dbm lookup of captured serial values
#if db.get(ibutton,0) != 0:
 #        print(str(db.get(ibutton)) + ' is the Command of ' + ibutton)
# else:
 #          print('I do not have command information for ' + ibutton)
  #         print('What is the command')
  #         command = input()
  #         db[ibutton] = command
   #        print('ibutton database updated.')
