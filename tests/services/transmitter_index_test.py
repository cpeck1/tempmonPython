"""
Testing interaction with transmitter cache and a fake list of USB devices
"""
import os, unittest
from unittest.mock import MagicMock

class FakeUsbDevice:
    def __init__(self, bus, address, idVendor, idProduct):
        self.bus = bus
        self.address = address
        self.idVendor = idVendor
        self.idProduct = idProduct

from bin.services.transmitter_index import (
    _TransmitterIdent, _TransmitterCache, TransmitterIndex
)

from tests.services.transmitter_index_test_dirs import (
    none, few_without_broken, few_with_broken, many_without_broken, 
    many_with_broken
)

class TransmitterIndexServiceTest(unittest.TestCase):
    def setUp(self):
        self.cache = _TransmitterCache()

        apn = os.path.abspath(none.__file__)
        self.cache_test_directory_none = (
            apn[:-len("__init__.py")] if apn.endswith("__init__.py") else apn
        )
        
        apnb = os.path.abspath(
            few_without_broken.__file__
        )
        self.cache_test_directory_few_without_broken = (
            apnb[:-len("__init__.py")] if apnb.endswith("__init__.py") else (
                apnb
            ) 
        )

        apfb = os.path.abspath(
            few_with_broken.__file__
        )
        self.cache_test_directory_few_with_broken = (
            apfb[:-len("__init__.py")] if apfb.endswith("__init__.py") else (
                apfb
            ) 
        )

        apm = os.path.abspath(many_without_broken.__file__)
        self.cache_test_directory_many_without_broken = (
            apm[:-len("__init__.py")] if apm.endswith("__init__.py") else apm
        )


        aphb = os.path.abspath(
            many_with_broken.__file__
        )
        self.cache_test_directory_many_with_broken = (
            aphb[:-len("__init__.py")] if aphb.endswith("__init__.py") else (
                aphb
            )
        )        

    def tearDown(self):
        pass

class TransmitterIndexServiceTestSuite(TransmitterIndexServiceTest):
    def test_cache_constructor0(self):
        self.cache.build(self.cache_test_directory_none)
        ids = []
        for item in self.cache.cache:
            ids.append(item.vendor_id)

        self.assertEqual(
            ids,
            []
        )

    def test_cache_constructor1(self):
        self.cache.build(self.cache_test_directory_few_without_broken)
        ids = []
        for item in self.cache.cache:
            ids.append(item.vendor_id)

        self.assertEqual(
            set(ids),
            {1, 2, 3, 4}
        )

    def test_cache_constructor2(self):
        self.cache.build(self.cache_test_directory_few_with_broken)
        ids = []
        for item in self.cache.cache:
            ids.append(item.vendor_id)

        self.assertEqual(
            set(ids),
            {1}
        )

    def test_cache_constructor3(self):
        self.cache.build(self.cache_test_directory_many_without_broken)
        ids = []
        for item in self.cache.cache:
            ids.append(item.vendor_id)

        self.assertEqual(
            set(ids),
            {1, 2, 3, 4, 5, 6, 7, 8, 9}
        )

    def test_cache_constructor4(self):
        self.cache.build(self.cache_test_directory_many_with_broken)
        ids = []
        for item in self.cache.cache:
            ids.append(item.vendor_id)

        self.assertEqual(
            ids,
            []
        )

    def test_cache_constructor5(self):
        self.cache.build("fake/ass/directory/that/in/no/way/could/exist/without/some/user/reading/this")
        
        self.assertEqual(
            self.cache.cache,
            []
        )

    # Test case: neither pid nor vid match
    def test_transmitter_id_matches1(self):
        i = 1
        j = 2

        ident = _TransmitterIdent(
            "TestManufacturer"+str(i),
            "TestName"+str(i),
            i, # vid
            i, # pid
            ["TestUnit" + str(i)],
            lambda x: x,
            lambda x: x,
            lambda x: x
        )
        
        device = FakeUsbDevice(j, j, j, j)

        self.assertFalse(ident.matches(device.idVendor, device.idProduct))

    # Test case: pid matches, vid doesn't match
    def test_transmitter_id_matches2(self):
        i = 1
        j = 2

        ident = _TransmitterIdent(
            "TestManufacturer"+str(i),
            "TestName"+str(i),
            i, # vid
            i, # pid
            ["TestUnit" + str(i)],
            lambda x: x,
            lambda x: x,
            lambda x: x
        )        
        
        device = FakeUsbDevice(j, j, i, j)

        self.assertFalse(ident.matches(device.idVendor, device.idProduct))

    # Test case: pid doesn't match, vid matches
    def test_transmitter_id_matches3(self):
        i = 1
        j = 2

        ident = _TransmitterIdent(
            "TestManufacturer"+str(i),
            "TestName"+str(i),
            i, # vid
            i, # pid
            ["TestUnit" + str(i)],
            lambda x: x,
            lambda x: x,
            lambda x: x
        )        
        
        device = FakeUsbDevice(j, j, j, i)

        self.assertFalse(ident.matches(device.idVendor, device.idProduct))

    # Test case: pid matches, vid matches
    def test_transmitter_id_matches4(self):
        i = 1
        j = 2

        ident = _TransmitterIdent(
            "TestManufacturer"+str(i),
            "TestName"+str(i),
            i, # vid
            i, # pid
            ["TestUnit" + str(i)],
            lambda x: x,
            lambda x: x,
            lambda x: x
        )        
        
        device = FakeUsbDevice(j, j, i, i)

        self.assertTrue(ident.matches(device.idVendor, device.idProduct))


    # Test case: >=1 devices, 0 transmitters defined
    def test_filter1(self):
        self.cache.build(self.cache_test_directory_none)
        
        devices = [FakeUsbDevice(i+1, i+1, i+1, i+1) for i in range(0, 25)]

        matching = TransmitterIndex.filter(devices, self.cache)
        
        ids = [x.vendor_id for x in matching]
        self.assertEqual(
            set(ids),
            set()
        )

    # Test case: 0 devices, >=1 transmitters defined, 0 matches
    def test_filter2(self):
        self.cache.build(self.cache_test_directory_few_without_broken)
        
        devices = [
        ]

        matching = TransmitterIndex.filter(devices, self.cache)
        
        ids = [x.vendor_id for x in matching]
        self.assertEqual(
            set(ids),
            set()
        )

    # Test case: >=1 devices, >=1 transmitters defined, 0 matches
    def test_filter3(self):
        self.cache.build(self.cache_test_directory_few_without_broken)
        
        devices = [
            FakeUsbDevice(15, 16, 2012, 4021),
            FakeUsbDevice(12, 19, 20123, 19421)
        ]

        matching = TransmitterIndex.filter(devices, self.cache)
        
        ids = [x.vendor_id for x in matching]
        self.assertEqual(
            set(ids),
            set()
        )

    # Test case: >=1 devices, >=1 transmitters defined, >=1 matches
    def test_filter4(self):
        self.cache.build(self.cache_test_directory_few_without_broken)
        
        devices = [
            FakeUsbDevice(1, 1, 1, 1),
            FakeUsbDevice(4, 4, 4, 4)
        ]

        matching = TransmitterIndex.filter(devices, self.cache)
        
        ids = [x.vendor_id for x in matching]
        self.assertEqual(
            set(ids),
            {1, 4}
        )

    # Test case: many devices, many transmitters defined, 0 matches
    def test_filter5(self):
        self.cache.build(self.cache_test_directory_many_without_broken)
        
        devices = [FakeUsbDevice(i+1, i+1, i+1, i+1) for i in range(
            100, 150, 1
        )]

        matching = TransmitterIndex.filter(devices, self.cache)
        
        ids = [x.vendor_id for x in matching]
        self.assertEqual(
            set(ids),
            set()
        )
     
    # Test case: many devices, many transmitters defined, many matches
    def test_filter6(self):
        self.cache.build(self.cache_test_directory_many_without_broken)
        
        devices = [FakeUsbDevice(i+1, i+1, i+1, i+1) for i in range(25)]

        matching = TransmitterIndex.filter(devices, self.cache)
        
        ids = [x.vendor_id for x in matching]
        self.assertEqual(
            set(ids),
            set([i+1 for i in range(9)])
        )
