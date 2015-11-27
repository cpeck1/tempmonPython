import unittest, pyudev, time
from unittest.mock import MagicMock, patch

from multiprocessing import Process

from bin.models.command import Command
from bin.models.usb_operation import UsbOperation
from bin.services.usb_library_translator import PyudevDevice
from bin.services.networking.message import (
    DocumentMessage,
    CommandMessage
)

from bin.controllers.transmitter_application_controller import (
    NEXT_CHILD_ID,
    REMOVE_CHILD_ID,
    _TransmitterApplication,
    TransmitterApplicationController
)

class TransmitterApplicationControllerTest(unittest.TestCase):
    def setUp(self):
        self.tap = TransmitterApplicationController()

    def tearDown(self):
        self.tap = None

class TransmitterApplicationControllerTestSuite(
        TransmitterApplicationControllerTest
):
    def test_next_child_id0(self):
        """NEXT_CHILD_ID should always return a unique ID"""
        ids = set()
        for _ in range(1000):
            ids.add(NEXT_CHILD_ID())

        self.assertEqual(len(ids), 1000)

    def test_next_child_id1(self):
        """NEXT_CHILD_ID should always return the lowest ID available"""
        for _ in range(1000):
            _ = NEXT_CHILD_ID()

        REMOVE_CHILD_ID(500)

        self.assertEqual(NEXT_CHILD_ID(), 500)

