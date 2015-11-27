"""
Mostly testing the open and close methods
"""
import unittest, random, json

from bin.infrastructure.usb_bus import UsbDevice
from bin.infrastructure.operation import Operation
from bin.models.usb_operation import UsbOperation

class UsbOperationTest(unittest.TestCase):
    def setUp(self):
        self.test_device = UsbDevice.from_attributes(
            path='/',
            bus=1,
            device=1,
            idVendor=12345,
            idProduct=54321,
            product='test_product',
            manufacturer='test_manufacturer'
        )
        self.test_operation = Operation('add')

    def tearDown(self):
        pass

class UsbOperationTestSuite(UsbOperationTest):
    def test_creation_from_json(self):
        """Usb Operation properly created from JSON string"""
        usb_operation = UsbOperation(self.test_operation, self.test_device)

        u_json = self.test_device.to_json()
        json_string = "{\"usb_device\": "+u_json+", "+"\"operation\": {\"value\": \"add\"}}"

        op = UsbOperation.from_json(json_string)
        self.assertEqual(op, usb_operation)

    def test_to_json(self):
        """Usb Operation's to_json method should create appropriate JSON string"""
        usb_operation = UsbOperation(self.test_operation, self.test_device)
        json_string = usb_operation.to_json()
        js_obj = json.loads(json_string)

        u_json = self.test_device.to_json()
        json_string_ctrl = "{\"usb_device\": "+u_json+", "+"\"operation\": {\"value\": \"add\"}}"
        js_obj_ctrl = json.loads(json_string_ctrl)

        # load the objects as json since ordering doesn't matter
        self.assertEqual(js_obj, js_obj_ctrl)
