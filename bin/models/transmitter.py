# from sqlalchemy import *
# from models.base import Base
# from sqlalchemy.orm import relationship

from bin.models.channel import Channel

class Transmitter:
    def __init__(
            self,
            bus,
            address,
            manufacturer,
            name,
            vendor_id,
            product_id,
            num_channels,
            channel_units,
            open_method=None,
            read_channel_method=None,
            close_method=None
    ):
        self.bus = bus
        self.address = address

        self.manufacturer = manufacturer
        self.name = name
        self.vendor_id = vendor_id
        self.product_id = product_id

        self.num_channels = num_channels
        self.channel_units = channel_units
        self.channels = []

        self.device_handle = None
        self.open_method = open_method
        self.read_channel_method = read_channel_method
        self.close_method = close_method

    def __repr__(self):
        return "Transmitter(bus={}, address={}, manufacturer={}, name={}, vendir_id={}, product_id={}, num_channels={}, channel_units={})".format(
            self.bus,
            self.address,
            self.manufacturer,
            self.name,
            self.vendor_id,
            self.product_id,
            self.num_channels,
            self.channel_units
        )

    def open(self):
        print(self.open_method)
        self.device_handle = self.open_method(
            self.bus,
            self.address
        )
        # propagate the device handle downward and give each channel
        # the means to read itself
        for i in range(self.num_channels):
            channel = Channel(
                bus = self.bus,
                address = self.address,
                channel_number = i+1,
                device_handle = self.device_handle,
                read_method = self.read_channel_method,
                units = self.channel_units[i]
            )
            self.channels.append(channel)

    def close(self):
        self.close_method(self.device_handle)
