# Device Name:
# The device's name; could be an abbreviation, just something for humans
# to identify the class of transmitter being used
name="EXAMPLE NAME"

# Device Manufacturer:
# The device's manufacturer; whoever assembles or sells the transmitter
# will do
manufacturer="EXAMPLE MANUFACTURER"

# Device ID:
# The device's vendor ID and product ID. Any format will do but
# be aware that most vendor and product IDs are presented in 
# hexadecimal format, for example the bash command lsusb returns IDs
# as ID XXXX:YYYY, which are actually in hexadecimal format despite
# not being preceded by a '0x', so writing idVendor=XXXX and 
# idProduct=YYYY will result in a syntax by Python; be sure to write 
# these instead as idVendor=0xXXXX and idProduct=0xYYYY
idVendor=0x0000
idProduct=0x0000

# Device Units:
# This one is a bit odd: the UNITS of the value returned by each of the
# transmitter's channels, in order from lowest channel to highest 
# channel. This is to accommodate any form of transmitter; note python
# shortcuts exist in the case where the transmitter has many channels
# that return the same unit, for example a transmitter with 120 
# temperature channels can have their channel_units written as:
channel_units=["Celsius"]*120
# or 30 temperature channels and 30 relative humidity channels may be
# written as (assuming channels 1-30 are temperature and 31-60 are 
# humidity):
channel_units=["Celsius"]*30 + ["Percent"]*30
# More than likely, however, the transmitter may only have a single 
# channel, in which case you would write:
channel_units=["Celsius"]

# Device Driver Package: 
# OPTION 1: driver_package_name
# The PACKAGE NAME of the driver package importable as a python module
# note that this is NOT the same as the absolute path to the package!
# handing Python a path to import will not succeed, therefore this
# option is only to be used if the driver package is somewhere within
# your python $PATH; a good test for whether this works is to open up 
# your python interpreter and import the string below using
# >>> __import__("package_name")
# if you see something like <module 'package_name' from ...> then it 
# works!
driver_package_name="package_name"

# Option 2: driver_package_path
# The ABSOLUTE PATH to the driver package in the filesystem; this is the
# directory heirarchy that contains the driver package the transmitter
# uses. 
driver_package_path="/path/to/driver_package"

# ---------- IMPORTANT: ----------
# If BOTH driver_package_name AND driver_package_path are defined,
# the system will opt to use the PATH over the package name. 

