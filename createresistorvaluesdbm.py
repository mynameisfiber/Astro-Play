import dbm
# open a DB. The c option opens in read/write mode and creates the file if needed.
db = dbm.open('resistorvalues', 'c')

# add an items
db["500"] = "f"
db["330"] = "b"
db["470"] = "10"
db["1023"] = "blank"
db["5678"] = "l"
db["6789"] = "90"

print('Database created')
# close and save
db.close()
