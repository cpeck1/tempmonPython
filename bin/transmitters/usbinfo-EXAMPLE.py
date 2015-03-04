# The device's name; could be an abbreviation, just something for humans
# to identify the class of transmitter being used
name="EXAMPLE NAME!"

# The device's manufacturer; whoever assembles or sells the transmitter
# will do
manufacturer="EXAMPLE MANUFACTURER"

# The device's vendor ID and product ID in HEX! Any format will do but
# be aware that most vendor and product IDs are presented in 
# hexadecimal format so if you want a decimal id you must convert it 
# yourself
idVendor=0x0000
idProduct=0x0000

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

# Driver Package: 
# OPTION 1: driver_package_name
# The PACKAGE NAME of the driver package importable as a python module
# note that this is NOT the same as the absolute path to the package!
# handing Python a path to import will not succeed, therefore this
# option is only to be used if the driver package is somewhere within
# your python $PATH
driver_package_name="package_name"
# Option 2: driver_package_path
# The ABSOLUTE PATH to the driver package in the filesystem; this is the
# directory heirarchy that contains the driver package the transmitter
# uses. 
driver_package_path="/path/to/driver_package"
# NOTE: if both driver_package_name AND driver_package_path are defined,
# the system will opt to use the PATH over the package name. 

