import os

product="Test2"
manufacturer="Test Manufacturer2"
idVendor=0x0002
idProduct=0x0002
channel_units=["TestUnit2"]
path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
driver_package_path=path+"driver_package.py"
