import os

product="This one broke"
manufacturer="All good so far"
idVendor=0x0001
idProduct=0x0001
channel_units=["Yup yup yup"]
path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
driver_package_path=path+"driver_package.py" # but this doesnt exist!
