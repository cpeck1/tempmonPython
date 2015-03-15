import os

name="Test1"
manufacturer="Test Manufacturer1"
idVendor=0x0001
idProduct=0x0001
channel_units=["TestUnit1"]
path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
driver_package_path=path+"driver_package.py"
