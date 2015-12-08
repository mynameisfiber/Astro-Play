import serial
import dbm
# open a DB. The c option opens in read/write mode and creates the file if needed.
db = dbm.open('ibuttondb', 'c')
# Define serial object on COM5 baud 115200
#arduino = serial.Serial('COM5', 115200, timeout=.1)
arduino = serial.Serial('COM9', 57600, timeout=.1)
while True:
	data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
	if data:
		print (data)
#Insert dbm lookup of captured serial values
#if db.get(ibutton,0) != 0:
 #        print(str(db.get(ibutton)) + ' is the Command of ' + ibutton)
# else:
 #          print('I do not have command information for ' + ibutton)
  #         print('What is the command')
  #         command = input()
  #         db[ibutton] = command
   #        print('ibutton database updated.')
