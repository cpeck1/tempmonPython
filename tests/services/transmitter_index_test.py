"""
Testing interaction with transmitter cache and a fake list of USB devices
"""
import os, unittest

from bin.services.transmitter_index import (
    _TransmitterCache, TransmitterIndex
)

from tests.services import transmitter_index_test_dir

class TransmitterIndexServiceTest(unittest.TestCase):
    def setUp(self):
        self.cache = _TransmitterCache()
        ap = os.path.abspath(transmitter_index_test_dir.__file__)
        self.cache_test_directory = (
            ap[:-len("__init__.py")] if ap.endswith("__init__.py") else ap
        )

    def tearDown(self):
        pass

class TransmitterIndexServiceTestSuite(TransmitterIndexServiceTest):
    def test_cache_constructor1(self):
        self.cache.build(self.cache_test_directory)
        ids = []
        for item in self.cache.cache:
            ids.append(item.vendor_id)

        self.assertEqual(ids, None)

    def test_cache_constructor2(self):
        pass

    def test_filter1(self):
        pass

    def test_filter2(self):
        pass
