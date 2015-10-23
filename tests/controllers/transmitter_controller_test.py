import unittest
from unittest.mock import MagicMock, patch

from bin.controllers.transmitter_controller import TransmitterController

from bin.models.transmitter import Transmitter
from bin.models.channel import Channel

from bin.services.transmitter_index import (
    _TransmitterIdent, _TransmitterCache, TransmitterIndex
)

class FakeDeviceHandle:
    def __init__(self, channel_read_values):
        self.channel_read_values = channel_read_values

    def __getitem__(self, key):
        return self.channel_read_values[key-1]

class TransmitterControllerTest(unittest.TestCase):
    def setUp(self):
        self.transmitter_controller = TransmitterController()

    def tearDown(self):
        pass

class TransmitterControllerTestSuite(TransmitterControllerTest):
    # Test case: no transmitters
    pass
