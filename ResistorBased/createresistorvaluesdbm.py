import dbm
# open a DB. The c option opens in read/write mode and creates the file if needed.
db = dbm.open('resistorvalues', 'c')

# add an items
db["108"] = "x"
db["373"] = "y"
db["78"] = "End"
db["604"] = "while"
db["930"] = "then"
db["45"] = "If"
db["55"] = ">"
db["326"] = "+"
db["871"] = "="
db["984"] = "<"
db["208"] = "f"
db["912"] = "r"
db["556"] = "90"
db["895"] = "45"
db["67"] = "30"
db["967"] = "1"
db["991"] = "10"
db["1001"] = "4"

print('Database created')
# close and save
db.close()
