"""
Mostly testing the open and close methods
"""
import unittest, random

from bin.models.transmitter import Transmitter
from bin.models.channel import Channel

class TransmitterModelTest(unittest.TestCase):
    def setUp(self):
        self.transmitter = Transmitter(
            bus=1,
            address=1,
            manufacturer="Test Manufacturer",
            name="Test Name",
            vendor_id=0,
            product_id=0,
            num_channels=1,
            channel_units=["Test"],
            open_method=None,
            read_channel_method=None,
            close_method=None
        )

    def tearDown(self):
        self.transmitter = None

class TransmitterModelTestSuite(TransmitterModelTest):
    def test_open1(self):
        self.transmitter.open_method = lambda x,y: x+y
        self.transmitter.open()
        
        # device_handle=bus+address
        self.assertEqual(self.transmitter.device_handle, 2)

    def test_open2(self):
        self.transmitter.open_method = lambda x, y: x + y
        self.transmitter.read_channel_method = lambda x: x
        
        self.transmitter.open() 
        # opened channels
        self.assertTrue(self.transmitter.channels)

    def test_open3(self):
        self.transmitter.open_method = lambda x, y: x + y
        func = lambda x: x
        self.transmitter.read_channel_method = func

        self.transmitter.open()
        channel = self.transmitter.channels[0]

        self.assertEqual(channel.read_method, func)

    def test_close1(self):
        def test_open_func(v1, v2):
            return v1+v2
        def test_close_func(value):
            return 0

        self.transmitter.open_method = test_open_func
        self.transmitter.close_method = test_close_func

        self.transmitter.open()

        self.transmitter.close()
        self.assertTrue(self.transmitter.device_handle is None)

    def test_close2(self):
        def test_open_func(v1, v2):
            return v1+v2
        def test_close_func(value):
            return 1

        self.transmitter.open_method = test_open_func
        self.transmitter.close_method = test_close_func

        self.transmitter.open()

        self.transmitter.close()
        self.assertTrue(self.transmitter.device_handle is None)
