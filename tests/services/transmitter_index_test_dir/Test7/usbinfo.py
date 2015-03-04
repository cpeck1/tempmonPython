import os

name="Test7"
manufacturer="Test Manufacturer7"
idVendor=0x0007
idProduct=0x0007
channel_units=["TestUnit7"]
path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
driver_package_path=path+"driver_package.py"
