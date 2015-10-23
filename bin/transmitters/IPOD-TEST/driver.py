import random

class iPodHandle:
    def __init__(self):
        self.value = random.random()

def open_method(bus, device):
    return iPodHandle()

def read_channel_method(device_handle, channel_number):
    return device_handle.value*channel_number

def close_method(device_handle):
    pass
