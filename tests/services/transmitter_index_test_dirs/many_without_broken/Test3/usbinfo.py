import os

name="Test3"
manufacturer="Test Manufacturer3"
idVendor=0x0003
idProduct=0x0003
channel_units=["TestUnit3"]
path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
driver_package_path=path+"driver_package.py"
