""" 
    Library to convert resistor values to string command values.
    Used for command dictionary; administrative; command definitions stored here as translation codex of sorts.
"""


# Key/value pair database structure
import dbm

# Open a DB. The c option opens in read/write mode and creates the file if needed.
db = dbm.open('resistorvalues', 'c')

# Placeholder
db["1023"] = "blank"

# Directions
db["500"] = "f"
db["330"] = "b"
db["5678"] = "l"
db["913"] = "r"

# Meatspace values
db["470"] = "10"
db["___"] = "20"
db["___"] = "30"
db["___"] = "40"
db["___"] = "50"
db["___"] = "60"
db["___"] = "70"
db["___"] = "80"
db["6789"] = "90"

# Programatic syntax
db["604"] = "while"
db["___"] = "for"
db["___"] = "if"
db["32"] = "end"
db["109"] = "x"
db["___"] = "y"
db["871"] = "="
db["___"] = "=="
db["___"] = "!="
db["984"] = "<"
db["___"] = ">"
db["___"] = "<="
db["___"] = ">="
db["326"] = "+"
db["___"] = "-"
db["___"] = "*"
db["___"] = "/"
db["___"] = "%"
db["___"] = "^" # "**"


# Programatic values
db["___"] = "0"
db["967"] = "1"
db["___"] = "2"
db["___"] = "3"
db["1001"] = "4"
db["___"] = "5"
db["___"] = "6"
db["___"] = "7"
db["___"] = "8"
db["___"] = "9"


print('Database created')

# Close and save
db.close()