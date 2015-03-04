import os

name="Test8"
manufacturer="Test Manufacturer8"
idVendor=0x0008
idProduct=0x0008
channel_units=["TestUnit8"]
path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
driver_package_path=path+"driver_package.py"
