import dbm
# open a DB. The c option opens in read/write mode and creates the file if needed.
db = dbm.open('resistorvalues', 'c')


with open("dummyoutput.txt", "r") as file_object:
#print (file_object.readline(6))
    data=file_object.readlines()
    for line in data:
        words = line.split(";")
        #print (line.rsplit(";"))

        # Ignore position information and pull out resistor values
        # Note every fourth item to compensate for word pairs
        for i in range(1,len(words),4):
            # print(words[i])
            # the get method has 2 vlues lookup, and what to return is no match in this case is `0`
            if db.get(words[i],0) != 0:
                cmd1 = db.get(words[i])
                cmd2 = db.get(words[i+2])
                space = b' '
                cmd = cmd1 + space + cmd2
                #print (cmd.decode('ascii'))
                print (cmd)
