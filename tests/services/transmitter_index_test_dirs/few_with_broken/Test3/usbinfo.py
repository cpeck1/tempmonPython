import os

name="This one also doesn't work!"
manufacturer="Boo!"
idVendor=0x0001
idProduct=0x0001
channel_units=["What's wrong with this one?"]
path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
driver_package_path=path+"driver_pakcage.py" # uh oh spaghettios!
