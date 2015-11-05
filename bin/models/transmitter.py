# from sqlalchemy import *
# from models.base import Base
# from sqlalchemy.orm import relationship

from bin.models.channel import Channel

class Transmitter:
    """Class representing a transmitter device with a USB interface.

    A device is defined as a transmitter if it satisfies the following
    conditions:
    1) Is capable of communicating at least one measurement determined
    at the time of communication representing some external state
    2) Each measurement consists of a single n-tuple whose elements
    together describe a single state. Singleton values are returned
    as elements without the brackets
    3) Each measurement communicated is associated with a unique context
    known as a CHANNEL, and the device is capable of reading one channel
    independently of another (TODO: consider implementing transmitters
    that read all channels simultaneously)
    4) Each channel communicates one and only one measurement

    Obvious examples of transmitters:
    1) Temperature logger - returns a single value representing the
    temperature of the environment that the device occupies
    2) High channel count temperature aquisition modules - usually have
    in the range of 1-100 temperature channels, each of which
    communicates with some kind of temperature probe to determine
    the temperatures of a number of environments
    3) Temperature & Humidity logger - has two channels, one for
    reporting temperature and one for reporting humidity

    Non-Obvious examples of transmitters:
    1) USB GPS dongle - transmits a 2-tuple with the first element
    representing latitude and the second element representing longitude;
    may also return latitude and longitude on separate channels
    2) ???

    Attributes:
    usb_device: the usb device this transmitter uses
    num_channels: the number of channels this device has
    channel_units: the list of units returned by the channels of this
    device, where channel_units[n] are the units returned by channel #n
    open_method: the method used to open this device
    read_channel_method: the method used to read channel #n of this
    device
    close_method: the method used to close this device
    """
    def __init__(
            self,
            usb_device,
            num_channels,
            channel_units,
            open_method=None,
            read_channel_method=None,
            close_method=None
    ):
        self.usb_device = usb_device

        self.num_channels = num_channels
        self.channel_units = channel_units
        self.channels = []

        self.device_handle = None
        self.open_method = open_method
        self.read_channel_method = read_channel_method
        self.close_method = close_method

    def __repr__(self):
        return "Transmitter(usb_device={}, num_channels={}, channel_units={})".format(
            self.usb_device,
            self.num_channels,
            self.channel_units
        )

    def open(self):
        self.device_handle = self.open_method(
            self.usb_device.bus,
            self.usb_device.device
        )
        # propagate the device handle downward to give each channel
        # the means to read itself
        for i in range(self.num_channels):
            channel = Channel(
                usb_device = self.usb_device,
                channel_number=i+1,
                device_handle=self.device_handle,
                read_method=self.read_channel_method,
                units=self.channel_units[i]
            )
            self.channels.append(channel)

    def close(self):
        self.close_method(self.device_handle)
        self.device_handle = None
