import logging, usb.core

logger = logging.getLogger("monitoring_application")

from bin.models.transmitter import Transmitter
from bin.services.transmitter_index import TransmitterIndex

class TransmitterController:
    def __init__(self):
        # load transmitters
        self.transmitters = TransmitterIndex.filter(
            [usb_device for usb_device in usb.core.find(find_all=True)]
        )
        self.channels = []
        
    def open_all_channels(self):
        channels = []
        for transmitter in self.transmitters:
            transmitter.open()
            channels = channels + transmitter.channels 
        logger.info("Opened channels: " + str(channels))
 
        return channels

    def close_all_channels(self):
        for transmitter in self.transmitters:
            transmitter.close() 
