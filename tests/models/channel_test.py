"""
Mostly testing the read_channel method
"""
import unittest, random

from bin.models.transmitter import Transmitter
from bin.models.channel import Channel
from bin.models.exceptions import *

class ChannelModelTest(unittest.TestCase):
    def setUp(self):
        class _DeviceHandleShell:
            def __init__(self):
                self.read_value = 14
        def _open_method(bus, address):
            return _DeviceHandleShell()

        self.transmitter = Transmitter(
            bus=1,
            address=1,
            manufacturer="Test Manufacturer",
            name="Test Name",
            vendor_id=0,
            product_id=0,
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
        self.transmitter.read_channel_method = 0

        self.transmitter.open()
        channel = self.transmitter.channels[0]
        
        try: 
            channel.read()
        except Exception as e:
            self.assertTrue(isinstance(e, InvalidReadMethod))

    def test_read2(self):
        self.transmitter.read_channel_method = lambda x, y: x + y
        
        self.transmitter.open()
        channel = self.transmitter.channels[0]
        
        channel.device_handle = None
        
        try:
            channel.read()
        except Exception as e:
            self.assertTrue(isinstance(e, NoDeviceHandle))

    def test_read3(self):
        self.transmitter.read_channel_method = lambda x, y: x + y

        self.transmitter.open()
        channel = self.transmitter.channels[0]
        
        channel.channel_number = None

        try:
            channel.read()
        except Exception as e:
            self.assertTrue(isinstance(e, NoChannelNumber))

    def test_read4(self):
        def _read_method(handle, channel_number):
            return handle.read_value

        self.transmitter.read_channel_method = _read_method
        
        self.transmitter.open()
        channel = self.transmitter.channels[0]
        value = channel.read()

        self.assertEqual(value, 14)
