"""
Mostly testing the read_channel method
"""
import unittest, random

from bin.models.transmitter import Transmitter
from bin.models.channel import Channel
from bin.models.exceptions import *

class FakeUsbDevice:
    def __init__(self):
        self.path = '/'
        self.bus = 1
        self.device = 1
        self.port = 1
        self.idVendor = 1
        self.idProduct = 1
        self.manufacturer = 'fake_manufacturer'
        self.product = 'fake_product'


class ChannelModelTest(unittest.TestCase):
    def setUp(self):
        class _DeviceHandleShell:
            def __init__(self):
                self.read_value = 14
        def _open_method(bus, port):
            return _DeviceHandleShell()

        self.transmitter = Transmitter(
            usb_device=FakeUsbDevice(),
            num_channels=1,
            channel_units=["Test"],
            open_method=_open_method,
            read_channel_method=None,
            close_method=None
        )

    def tearDown(self):
        self.transmitter = None

class ChannelModelTestSuite(ChannelModelTest):
    def test_read1(self):
        """Channel raises InvalidReadMethodError with bad read method"""
        self.transmitter.read_channel_method = 0

        self.transmitter.open()
        channel = self.transmitter.channels[0]

        with self.assertRaises(InvalidReadMethodError):
            channel.read()

    def test_read2(self):
        """Channel raises NoDeviceHandleError when reading without device handle"""
        self.transmitter.read_channel_method = lambda x, y: x + y

        self.transmitter.open()
        channel = self.transmitter.channels[0]

        channel.device_handle = None

        with self.assertRaises(NoDeviceHandleError):
            channel.read()

    def test_read3(self):
        """Channel raises NoChannelNumberError reading without a channel number"""
        self.transmitter.read_channel_method = lambda x, y: x + y

        self.transmitter.open()
        channel = self.transmitter.channels[0]

        channel.channel_number = None

        try:
            channel.read()
        except Exception as e:
            self.assertTrue(isinstance(e, NoChannelNumberError))

    def test_read4(self):
        """Channel reads properly if constructed properly"""
        def _read_method(handle, channel_number):
            return handle.read_value

        self.transmitter.read_channel_method = _read_method

        self.transmitter.open()
        channel = self.transmitter.channels[0]
        value = channel.read()

        self.assertEqual(value, 14)
