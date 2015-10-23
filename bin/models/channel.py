import json, logging
from bin.models.exceptions import *
from datetime import datetime

logger = logging.getLogger("monitoring_application")

class Channel:
    """A single channel of a transmitter object. The channel contains
    information about some external state, and

    Attributes:
    bus: the USB bus this channel is plugged into
    address: the USB address of the bus this channel is plugged into
    channel_number: the channel number of the transmitter to which this
    channel belongs
    device_handle: the device handle of the transmitter object so that
    each channel may read itself
    units: the units that this channel associates to any value it
    gathers from a reading
    """
    def __init__(
            self,
            usb_device,
            channel_number,
            device_handle,
            read_method,
            units
    ):
        self.usb_device = usb_device
        self.channel_number = channel_number
        self.device_handle = device_handle
        self.read_method = read_method
        self.units = units

        self.current_state_value = None
        self.last_update_time = None

    def read(self):
        """read this channel using the tools given by the transmitter"""
        if (not callable(self.read_method)):
            raise InvalidReadMethodError
        if self.device_handle is None:
            raise NoDeviceHandleError
        if self.channel_number is None:
            raise NoChannelNumberError
        try:
            return self.read_method(self.device_handle, self.channel_number)
        except TypeError:
            # so read_method is callable but does not take 2 arguments
            raise InvalidReadMethodError

    def update(self):
        """attempt to update this channel's state and return whether
        an update occurred
        """
        try:
            read_value = self.read()
        except:
            logger.error(
                "Critical driver error in channel "+repr(self)
            )
        if read_value:
            self.current_state_value = read_value
            self.last_update_time = datetime.now().isoformat()
            return True # indicate state updated
        return False # implied by None but bool return type instead
