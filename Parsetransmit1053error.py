import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = '192.168.0.48'                          
port = 9999
# connection to hostname on the port.
s.connect((host, port))                               
import dbm
# open a DB. The c option opens in read/write mode and creates the file if needed.
db = dbm.open('resistorvalues', 'c')



#Use `with` to open canned serial string text
# need to switch to serial read in real program
with open("dummyoutput.txt", "r") as file_object:
#assign all lines to data variable
    data=file_object.readlines()
    # Walk through the lines to pull out words on individual lines
    for line in data:
        words = line.split(";")
        # Ignore position information and pull out resistor values
        # Note every fourth item to compensate for word pairs
        for i in range(1,len(words),4):
            # print(words[i])

            #lookup command based on resistor value
            # the get method has 2 values, lookup, and what to return is no match in this case is `0`
            if db.get(words[i],0) != 0:
                cmd1 = db.get(words[i])
                cmd2 = db.get(words[i+2])
                space = b' '
                cmd = cmd1 + space + cmd2
            #Use already open port to send data
                s.send(cmd)
            # Receive no more than 1024 bytes
                tm = s.recv(1024)                                     
s.close()

print("Robot command processed is %s" % tm.decode('ascii'))
