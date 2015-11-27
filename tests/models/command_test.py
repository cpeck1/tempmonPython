"""
Mostly testing the open and close methods
"""
import unittest, random

from bin.models.command import Command

class CommandTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

class CommandTestSuite(CommandTest):
    def test_bad_command1(self):
        """Command raises ValueError when instantiating (via value) bad command"""
        with self.assertRaises(ValueError):
            command = Command('Fake Command1')

    def test_bad_command2(self):
        """Command raises KeyError when instantiating (via key) bad command """
        with self.assertRaises(KeyError):
            command = Command['Fake Command2']

    def test_status_command(self):
        """Command.STATUS is a valid Command"""
        # make sure STATUS is a valid command
        command = Command('STATUS')
        self.assertTrue(type(command) == Command)

    def test_void_command(self):
        """Command.VOID is a valid Command"""
        # make sure VOID is a valid command
        command = Command('VOID')
        self.assertTrue(type(command) == Command)

    def test_shutdown_command(self):
        """Command.SHUTDOWN is a valid Command"""
        # make sure SHUTDOWN is a valid command
        command = Command('SHUTDOWN')
        self.assertTrue(type(command) == Command)

    def test_serialize_deserialize1(self):
        """Command successfully reconstructed after serialization/deserialization"""
        for command in Command:
            serialized = command.serialize()
            deserialized = Command.deserialize(serialized)
            self.assertTrue(deserialized is command)
