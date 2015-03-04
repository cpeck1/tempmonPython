from .reading import Reading
from .exceptions import *

class Channel:
    def __init__(
            self, 
            bus, 
            address, 
            channel_number, 
            device_handle, 
            read_method,
            units
    ):
        self.id = None
        self.bus = bus
        self.address = address
        self.channel_number = channel_number
        self.device_handle = device_handle
        self.read_method = read_method
        self.units = units
        
    def read(self):
        if (not callable(self.read_method)):
            raise InvalidReadMethod
        if self.device_handle is None:
            raise NoDeviceHandle
        if self.channel_number is None:
            raise NoChannelNumber
        return self.read_method(self.device_handle, self.channel_number)
