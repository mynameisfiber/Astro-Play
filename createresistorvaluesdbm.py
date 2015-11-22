""" 
    Library to convert resistor values to string command values.
    Used for command dictionary; administrative; command definitions stored here as translation codex of sorts.
"""


# Key/value pair database structure
import dbm

# Open a DB. The c option opens in read/write mode and creates the file if needed.
db = dbm.open('resistorvalues', 'c')

# Directions
db["500"] = "f"
db["330"] = "b"
db["1023"] = "blank"
db["5678"] = "l"
# Values
db["470"] = "10"
db["6789"] = "90"
# Programatic syntax
db["604"] = "while"
#db["XXX"] = "for"
#db["YYY"] = "in"
#db["ZZZ"] = "if"

print('Database created')

# Close and save
db.close()