import unittest
from unittest.mock import MagicMock
from datetime import datetime
import time

from transmitter import Transmitter

class TransmitterTest(unittest.TestCase):
    def setUp(self):
        self.transmitter = Transmitter(1342)
        
    def tearDown(self):
        self.transmitter = None

class TransmitterMockList(unittest.TestCase):
    def setUp(self):
        def open_device(x, y): return [-80]
        def read_device(x): return x[0]
        def close_device(x): x = None

        self.transmitter = Transmitter(12345, "Man", "Nam", 1, 1)

        self.transmitter.set_open_method(open_device)
        self.transmitter.set_read_method(read_device)
        self.transmitter.set_close_method(close_device)

    def tearDown(self):
        if self.transmitter.is_open():
            self.transmitter.close()
        self.transmitter = None

class DefaultUninitializedStateTest(TransmitterTest):
    def test_default_container_id(self):
        cid = self.transmitter.container_id
        self.assertEqual(
            cid, 1342,
            "did not match expected default value")

    def test_default_manufacturer(self):
        man = self.transmitter.manufacturer
        self.assertEqual(
            man, None,
            "did not match expected default value")

    def test_default_name(self):
        name = self.transmitter.name
        self.assertEqual(
            name, None,
            "did not match expected default value")

    def test_default_vendor_id(self):
        vid = self.transmitter.vendor_id
        self.assertEqual(
            vid, None,
            "did not match expected default value")

    def test_default_product_id(self):
        pid = self.transmitter.product_id
        self.assertEqual(
            pid, None,
            "did not match expected default value")

    def test_default_device(self):
        self.assertEqual(
            self.transmitter._device, None,
            "did not match expected default value")

    def test_default_open_method(self):
        self.assertEqual(
            self.transmitter._open_method, None,
            "did not match expected default value")

    def test_default_read_method(self):
        self.assertEqual(
            self.transmitter._read_method, None,
            "did not match expected default value")

    def test_default_open_method(self):
        self.assertEqual(
            self.transmitter._close_method, None,
            "did not match expected default value")


class AccessorTest(TransmitterTest):
    def test_get_set_manufacturer1(self):
        man_set = ""
        self.transmitter.manufacturer = man_set
        man_get = self.transmitter.manufacturer
        self.assertEqual(
            man_set, man_get,
            "set value '" + str(man_set) + 
            "' did not match get value '" + str(man_get)+"'")

    def test_get_set_manufacturer2(self):
        man_set = "get set manufacturer test 2"
        self.transmitter.manufacturer = man_set
        man_get = self.transmitter.manufacturer
        self.assertEqual(
            man_set, man_get,
            "set value '" + str(man_set) + 
            "' did not match get value '" + str(man_get)+"'")

    def test_get_set_manufacturer3(self):
        man_set = "really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really long set value"
        self.transmitter.manufacturer = man_set
        man_get = self.transmitter.manufacturer
        self.assertEqual(
            man_set, man_get,
            "set value '" + str(man_set) + 
            "' did not match get value '" + str(man_get)+"'")

    def set_manufacturer(self, man):
        self.transmitter.manufacturer = man

    def test_set_manufacturer_bad_type1(self):
        man_set = None
        self.assertRaises(
            AssertionError, self.set_manufacturer, man_set)

    def test_set_manufacturer_bad_type2(self):
        man_set = 123456
        self.assertRaises(
            AssertionError, self.set_manufacturer, man_set)

    def test_set_manufacturer_bad_type3(self):
        man_set = ["list of", "manufacturers"]
        self.assertRaises(
            AssertionError, self.set_manufacturer, man_set)

    def test_get_set_name1(self):
        name_set = ""
        self.transmitter.name = name_set
        name_get = self.transmitter.name
        self.assertEqual(
            name_set, name_get,
            "set value '" + str(name_set) + 
            "' did not match get value '" + str(name_get)+"'")

    def test_get_set_name2(self):
        name_set = "test get set name 2"
        self.transmitter.name = name_set
        name_get = self.transmitter.name
        self.assertEqual(
            name_set, name_get,
            "set value '" + str(name_set) + 
            "' did not match get value '" + str(name_get)+"'")

    def test_get_set_name3(self):
        name_set = "really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really long name set value"
        self.transmitter.name = name_set
        name_get = self.transmitter.name
        self.assertEqual(
            name_set, name_get,
            "set value '" + str(name_set) + 
            "' did not match get value '" + str(name_get)+"'")

    def set_name(self, name):
        self.transmitter.name = name

    def test_set_name_bad_type1(self):
        name_set = None
        self.assertRaises(
            AssertionError, self.set_name, name_set)

    def test_set_name_bad_type2(self):
        name_set = 123456
        self.assertRaises(
            AssertionError, self.set_name, name_set)

    def test_set_name_bad_type3(self):
        name_set = ["a list of", "names for some reason"]
        self.assertRaises(
            AssertionError, self.set_name, name_set)

    def test_get_set_vendor_id1(self):
        id_set = 0x0001
        self.transmitter.vendor_id = id_set
        id_get = self.transmitter.vendor_id
        self.assertEqual(
            id_set, id_get,
            "set value '" + str(id_set) + 
            "' did not match get value '" + str(id_get)+"'")

    def test_get_set_vendor_id2(self):
        id_set = 0x1048
        self.transmitter.vendor_id = id_set
        id_get = self.transmitter.vendor_id
        self.assertEqual(
            id_set, id_get,
            "set value '" + str(id_set) + 
            "' did not match get value '" + str(id_get)+"'")

    def test_get_set_vendor_id3(self):
        id_set = 0xFFFF
        self.transmitter.vendor_id = id_set
        id_get = self.transmitter.vendor_id
        self.assertEqual(
            id_set, id_get,
            "set value '" + str(id_set) + 
            "' did not match get value '" + str(id_get)+"'")

    def set_vendor_id(self, vid):
        self.transmitter.vendor_id = vid
        
    def test_set_vendor_id_bad_range1(self):
        id_set = 0x0000
        self.assertRaises(
            AssertionError, self.set_vendor_id, id_set)

    def test_set_vendor_id_bad_range2(self):
        id_set = 0x10000
        self.assertRaises(
            AssertionError, self.set_vendor_id, id_set)

    def test_set_vendor_id_bad_range3(self):
        id_set = -0xA2E7
        self.assertRaises(
            AssertionError, self.set_vendor_id, id_set)
        
    def test_set_vendor_id_bad_type1(self):
        id_set = None
        self.assertRaises(
            AssertionError, self.set_vendor_id, id_set)

    def test_set_vendor_id_bad_type2(self):
        id_set = 123.156
        self.assertRaises(
            AssertionError, self.set_vendor_id, id_set)

    def test_set_vendor_id_bad_type3(self):
        id_set = ["list of", "vendor ids wtf?"]
        self.assertRaises(
            AssertionError, self.set_vendor_id, id_set)
        

    def test_get_set_product_id1(self):
        id_set = 0x0001
        self.transmitter.product_id = id_set
        id_get = self.transmitter.product_id
        self.assertEqual(
            id_set, id_get,
            "set value '" + str(id_set) + 
            "' did not match get value '" + str(id_get)+"'")

    def test_get_set_product_id2(self):
        id_set = 0x1048
        self.transmitter.product_id = id_set
        id_get = self.transmitter.product_id
        self.assertEqual(
            id_set, id_get,
            "set value '" + str(id_set) + 
            "' did not match get value '" + str(id_get)+"'")

    def test_get_set_product_id3(self):
        id_set = 0xFFFF
        self.transmitter.product_id = id_set
        id_get = self.transmitter.product_id
        self.assertEqual(
            id_set, id_get,
            "set value '" + str(id_set) + 
            "' did not match get value '" + str(id_get)+"'")

    def set_product_id(self, pid):
        self.transmitter.product_id = pid

    def test_set_product_id_bad_range1(self):
        id_set = 0x0000
        self.assertRaises(
            AssertionError, self.set_product_id, id_set)

    def test_set_product_id_bad_range2(self):
        id_set = 0x10000
        self.assertRaises(
            AssertionError, self.set_product_id, id_set)

    def test_set_product_id_bad_range3(self):
        id_set = -0xA2E7
        self.assertRaises(
            AssertionError, self.set_product_id, id_set)
        
    def test_set_product_id_bad_type1(self):
        id_set = None
        self.assertRaises(
            AssertionError, self.set_product_id, id_set)

    def test_set_product_id_bad_type2(self):
        id_set = 123.156
        self.assertRaises(
            AssertionError, self.set_product_id, id_set)

    def test_set_product_id_bad_type3(self):
        id_set = ["list of", "product ids wtf?"]
        self.assertRaises(
            AssertionError, self.set_product_id, id_set)

class BooleanFunctionTests(TransmitterTest):
    def vid_pid_valid_test1(self):
        self.assertFalse(
            self.transmitter.vid_pid_valid(),
            "not initially False as expected")

    def vid_pid_valid_test2(self):
        self.transmitter.vendor_id = 0x1234
        self.assertFalse(
            self.transmitter.vid_pid_valid(),
            "invalid product_id yielded false positive")


    def vid_pid_valid_test3(self):
        self.transmitter.set_product_id(0x4321)
        self.assertFalse(
            self.transmitter.vid_pid_valid(),
            "invalid vendor_id yielded false positive")

    def vid_pid_valid_test3(self):
        self.transmitter.vendor_id = 0x1234
        self.transmitter.product_id = 0x4321
        self.assertTrue(
            self.transmitter.vid_pid_valid(),
            "valid vendor_id and product_id yielded false negative")

    def method_available_test1(self):
        self.assertFalse(
            self.transmitter.method_available('open'),
            "invalid open method yielded false positive")

    def method_available_test2(self):
        self.assertFalse(
            self.transmitter.method_available('read'),
            "invalid read method yielded false positive")

    def method_available_test3(self):
        self.assertFalse(
            self.transmitter.method_available('close'),
            "invalid close method yielded false positive")

    def method_available_test4(self):
        self.transmitter.set_open_method(print)
        self.assertTrue(
            self.transmitter.method_available('open'),
            "valid open method yielded false negative")

    def method_available_test5(self):
        self.transmitter.set_read_method(print)
        self.assertTrue(
            self.transmitter.method_available('read'),
            "valid read method yielded false negative")

    def method_available_test6(self):
        self.transmitter.set_close_method(print)
        self.assertTrue(
            self.transmitter.method_available('close'),
            "valid close method yielded false negative")


class ListMockTest(TransmitterMockList):
    """
    tests where the transmitter operations involve the setting and returning
    of a simple list

    open(): returns [-80.0]
    read(): returns _device[0]
    close(): sets _device = None
    """
    def test_open1(self):
        self.transmitter.open()
        self.assertTrue(
            self.transmitter.is_open(), 
            "did not open as expected")

    def test_open2(self):
        self.transmitter.open()
        self.transmitter.open()
        self.assertTrue(
            self.transmitter.is_open(),
            "did not remain open as expected")

    def test_open3(self):
        self.transmitter.open()
        self.transmitter.close()
        self.transmitter.open()
        self.assertTrue(
            self.transmitter.is_open(),
            "did not reopen as expected")            

    def test_read1(self):
        self.transmitter.open()
        reading = self.transmitter.read()
        self.assertEqual(
            reading, -80,
            "did not produce expected output")
        
    def test_read2(self):
        self.transmitter.open()
        self.transmitter.open()
        reading = self.transmitter.read()
        self.assertEqual(
            reading, -80,
            "did not produce expected output")

    def test_read3(self):
        self.transmitter.open()
        self.transmitter.close()
        self.transmitter.open()
        reading = self.transmitter.read()
        self.assertEqual(
            reading, -80,
            "did not produce expected output")

    def test_close1(self):
        self.transmitter.open()
        self.transmitter.close()
        self.assertFalse(
            self.transmitter.is_open(),
            "did not close device as expected")

    def test_close2(self):
        self.transmitter.open()
        self.transmitter.close()
        self.transmitter.open()
        self.transmitter.close()
        self.assertFalse(
            self.transmitter.is_open(),
            "did not close device as expected")
