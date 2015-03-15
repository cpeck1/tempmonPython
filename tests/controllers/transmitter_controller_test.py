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
    def test_open_all_channels1(self):
        self.transmitter_controller.transmitters  = []

        channels = self.transmitter_controller.open_all_channels()
        self.assertEqual(channels, [])
        
    # Test case: single transmitter, single channel
    def test_open_all_channels2(self):
        transmitter = Transmitter(
            bus = 0,
            address = 1,
            manufacturer = "TestManufacturer",
            name = "Test Name",
            vendor_id = 0x0001,
            product_id = 0x0002,
            num_channels = 1,
            channel_units = ["TestUnits"],
        )

        transmitter.open_method = MagicMock(
            return_value=FakeDeviceHandle([100])
        )

        transmitter.read_channel_method = lambda x, y: x[y]

        self.transmitter_controller.transmitters = [
            transmitter
        ]

        channels = self.transmitter_controller.open_all_channels()
        self.assertEqual(len(channels), 1)

        self.assertEqual(channels[0].read(), 100)

    # Test case: single transmitter, many channels
    def test_open_all_channels3(self):
        transmitter = Transmitter(
            bus = 0,
            address = 1,
            manufacturer = "TestManufacturer",
            name = "Test Name",
            vendor_id = 0x0001,
            product_id = 0x0002,
            num_channels = 1,
            channel_units = ["TestUnits"],
        )

        transmitter.open_method = MagicMock(
            return_value=FakeDeviceHandle([100])
        )

        transmitter.read_channel_method = lambda x, y: x[y]

        self.transmitter_controller.transmitters = [
            transmitter
        ]

        channels = self.transmitter_controller.open_all_channels()
        self.assertEqual(len(channels), 1)

        self.assertEqual(
            channels[0].read(), 100
        )

    # Test case: many transmitters, single channel (each)
    def test_open_all_channels4(self): 
        open_method = MagicMock(
            return_value=FakeDeviceHandle([100])
        ) 
        read_channel_method = lambda x, y: x[y]

        self.transmitter_controller.transmitters = [
            Transmitter(
                bus = i,
                address = i+1,
                manufacturer = "TestManufacturer",
                name = "Test Name",
                vendor_id = 0x0001,
                product_id = 0x0002,
                num_channels = 1,
                channel_units = ["TestUnits"],
                open_method = open_method,
                read_channel_method = read_channel_method
            ) for i in range(30)
        ]

        channels = self.transmitter_controller.open_all_channels()
        self.assertEqual(len(channels), 30)

        readings = [channels[i].read() for i in range(30)]
        self.assertEqual(readings, [100]*30)

    # Test case: many transmitters, many channels (each)
    def test_open_all_channels5(self):
        open_method = MagicMock(
            return_value=FakeDeviceHandle([100]*10)
        )
        read_channel_method = lambda x, y: x[y]

        self.transmitter_controller.transmitters = [
            Transmitter(
                bus = i,
                address = i+1,
                manufacturer = "TestManufacturer",
                name = "Test Name",
                vendor_id = 0x0001,
                product_id = 0x0002,
                num_channels = 10,
                channel_units = ["TestUnits"]*10,
                open_method = open_method,
                read_channel_method = read_channel_method
            ) for i in range(10)
        ]

        channels = self.transmitter_controller.open_all_channels()
        self.assertEqual(len(channels), 100)

        readings = [channels[i].read() for i in range(100)]
        self.assertEqual(readings, [100]*100)
