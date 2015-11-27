"""
Mostly testing the open and close methods
"""
import unittest, random

from bin.infrastructure.operation import Operation

class OperationTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

class OperationTestSuite(OperationTest):
    def test_bad_operation0(self):
        """Operation instantiated with bad operation via value raises ValueError"""
        with self.assertRaises(ValueError):
            operation = Operation('Bad Operation')

    def test_bad_operation1(self):
        """Operation instantiated with bad operation via name raises KeyError"""
        with self.assertRaises(KeyError):
            operation = Operation['Bad Operation']

    def test_add_operation(self):
        """Operation.ADD is a valid operation"""
        operation = Operation('add')
        self.assertTrue(type(operation) == Operation)

    def test_remove_operation(self):
        """Operation.REMOVE is a valid operation"""
        operation = Operation('remove')
        self.assertTrue(type(operation == Operation))

    def test_change_operation(self):
        """Operation.CHANGE is a valid operation"""
        operation = Operation('change')
        self.assertTrue(type(operation == Operation))

    def test_online_operation(self):
        """Operation.ONLINE is a valid operation"""
        operation = Operation('online')
        self.assertTrue(type(operation == Operation))

    def test_offline_operation(self):
        """Operation.OFFLINE is a valid operation"""
        operation = Operation('offline')
        self.assertTrue(type(operation == Operation))

    def test_serialize_deserialize(self):
        """Operation serialized and deserialized results in the same operation"""
        operation = Operation('add')
        new_operation = Operation.deserialize(operation.serialize())

        self.assertEqual(operation, new_operation)
