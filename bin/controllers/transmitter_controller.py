import usb.core

from models.transmitter import Transmitter
from services.transmitter_index import TransmitterIndex

class TransmitterController:
    def __init__(self, dbsession):
        # load transmitters
        self.dbsession = dbsession

        self.transmitters = TransmitterIndex.filter(
            [usb_device for usb_device in usb.core.find(find_all=True)]
        )
        
    def open_all_channels(self):
        channels = []
        for transmitter in self.transmitters:
            transmitter.open()
            channels = channels + transmitter.channels

        return channels
