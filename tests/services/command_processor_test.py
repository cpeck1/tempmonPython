import unittest, time, uuid, json
from unittest.mock import MagicMock, patch

from bin.models.command import Command
from bin.models.exceptions import ExitProcess
from bin.services.command_processor import CommandProcessor

class TestStruct:
    @classmethod
    def from_json(cls, json_string):
        dct = json.loads(json_string)
        return cls(
            a=dct['a'],
            b=dct['b'],
            c=dct['c'],
            d=dct['d'],
            e=dct['e'],
            f=dct['f'],
        )

    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        truthiness = (
            self.a == other.a and
            self.b == other.b and
            self.c == other.c and
            self.d == other.d and
            self.e == other.e and
            self.f == other.f
        )
        return truthiness

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class CommandProcessorTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

class CommandProcessorTestSuite(CommandProcessorTest):
    def test_process_status0(self):
        # classes without to_json should raise errors
        """Processing STATUS of None raises Exception"""
        status_object = None
        command_processor = CommandProcessor(status_object)

        with self.assertRaises(AttributeError):
            command = Command('STATUS')
            status = command_processor.process(command)

    def test_process_status1(self):
        """Processing STATUS of TestStruct returns JSON to reconstruct TestStruct"""
        status_object = TestStruct('a', 'b', 'c', 'd', 'e', 'f')
        command_processor = CommandProcessor(status_object)

        command = Command('STATUS')
        status = command_processor.process(command)

        status_object_reconstructed = TestStruct.from_json(status)
        self.assertEqual(
            status_object,
            status_object_reconstructed
        )

    def test_process_void0(self):
        """Processing VOID does nothing"""
        void_object = None
        command_processor = CommandProcessor(void_object)

        command = Command('VOID')
        void = command_processor.process(command)

        self.assertEqual(void, None)

    def test_process_shutdown1(self):
        """Processing SHUTDOWN with None raises ExitProcess"""
        # make sure the processor raises exception with any object
        shutdown_object = None
        command_processor = CommandProcessor(shutdown_object)

        command = Command('SHUTDOWN')

        with self.assertRaises(ExitProcess):
            command_processor.process(command)

    def test_process_shutdown1(self):
        """Processing SHUTDOWN of TestStruct raises ExitProcess"""
        # make sure the processor raises exception with fake struct
        shutdown_object = TestStruct('a', 'b', 'c', 'd', 'e', 'f')

        command_processor = CommandProcessor(shutdown_object)

        command = Command('SHUTDOWN')

        with self.assertRaises(ExitProcess):
            command_processor.process(command)
