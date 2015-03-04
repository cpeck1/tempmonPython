# from sqlalchemy import *
# from models.base import Base
# from sqlalchemy.orm import relationship

from .channel import Channel

class Transmitter:
    # __tablename__ = 'transmitter'

    # id = Column(Integer, primary_key=True)
    # bus = Column(Integer)
    # device = Column(Integer)
    # product_name = Column(String)
    # vendor_name = Column(String)
    # product_id = Column(Integer)
    # vendor_id = Column(Integer)

    # channels = relationship("Channel", backref='transmitter',
    #                         cascade="all, delete, delete-orphan")
    
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
            open_method,
            read_channel_method,
            close_method
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
        return "Transmitter(id={!r}, bus={!r}, name={!r}, manufacturer={!r}, product_id={!r}, vendor_id={!r}, channels={!r})".format(self.id, self.bus, self.device, self.name, self.manufacturer, self.product_id, self.vendor_id, self.channels)

    def __str__(self):
        s = "Transmitter: \n\t"
        s = s + "id: {!r} \n\t".format(self.id)
        s = s + "bus: {!r} \n\t".format(self.bus)
        s = s + "device: {!r} \n\t".format(self.device)
        s = s + "name: {!r} \n\t".format(self.name)
        s = s + "manufacturer: {!r} \n\t".format(self.manufacturer)
        s = s + "product_id: {!r} \n\t".format(self.product_id)
        s = s + "vendor_id: {!r} \n\t".format(self.vendor_id)

        s = s + "channels: \n\t"
        for c in self.channels:
            s = s + "channels: {} \n\t".format(str(c).replace("\n", "\n\t"))
            
        return s

    def open(self):
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
        if (self.close_method(self.device_handle) == 0):
            self.device_handle = None
