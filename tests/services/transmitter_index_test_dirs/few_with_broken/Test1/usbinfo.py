import os 

product="This one works!"
manufacturer="Hooray!"
idVendor=0x0001
idProduct=0x0001
channel_units=["TestUnit"]
path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
driver_package_path=path+"driver_package.py"

