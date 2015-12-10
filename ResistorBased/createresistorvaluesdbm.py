import dbm
# open a DB. The c option opens in read/write mode and creates the file if needed.
db = dbm.open('resistorvalues', 'c')

# add an items
db["108"] = "x"
db["373"] = "y"
<<<<<<< HEAD
<<<<<<< HEAD
db["247"] = "end"
db["604"] = "while"
db["930"] = "then"
db["45"] = "If"
db["55"] = "<"
db["326"] = "+"
db["871"] = "="
db["984"] = ">"
=======
=======
>>>>>>> 0d585fa268d365eb63ad52d1eeaf81ef74892fa4
db["78"] = "End"
db["604"] = "while"
db["930"] = "then"
db["45"] = "If"
db["55"] = ">"
db["326"] = "+"
db["871"] = "="
db["984"] = "<"
<<<<<<< HEAD
>>>>>>> 3cd7fd5b3fda1aa98f9bd25c062a85734facd1f7
=======
>>>>>>> 0d585fa268d365eb63ad52d1eeaf81ef74892fa4
db["208"] = "f"
db["912"] = "r"
db["556"] = "90"
db["895"] = "45"
db["67"] = "30"
db["967"] = "1"
db["991"] = "10"
<<<<<<< HEAD
<<<<<<< HEAD
db["463"] = "4"
=======
db["1001"] = "4"
>>>>>>> 3cd7fd5b3fda1aa98f9bd25c062a85734facd1f7
=======
db["1001"] = "4"
>>>>>>> 0d585fa268d365eb63ad52d1eeaf81ef74892fa4

print('Database created')
# close and save
db.close()
