import os

name="Test4"
manufacturer="Test Manufacturer4"
idVendor=0x0004
idProduct=0x0004
channel_units=["TestUnit4"]
path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
driver_package_path=path+"driver_package.py"
