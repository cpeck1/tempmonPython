import unittest, time, uuid, json
from unittest.mock import MagicMock, patch
from bin.services.networking.message import (
    APP_NAME,
    VERSION,
    DELIMITER,
    Message,
    CommandMessage,
    DocumentMessage
)

class TestStruct:
    """
    idealized structure with functional from_json and to_json methods
    assume attributes consist only of basic non-array python types
    """
    @classmethod
    def from_json(cls, json_object):
        if type(json_object) == str:
            dct = json.loads(json_object)
        elif type(json_object) == dict:
            dct = json_object

        return cls(
            a=int(dct['a']),
            b=float(dct['b']),
            c=str(dct['c']),
            d=bool(dct['d']),
            e=int(dct['e'])
        )

    def __init__(self, a, b, c, d, e):
        assert type(a) == int
        self.a = a # int

        assert type(b) == float
        self.b = b # float

        assert type(c) == str
        self.c = c # string

        assert type(d) == bool
        self.d = d # bool

        assert type(e) == int
        self.e = e # int

    def __eq__(self, other):
        truthiness = (
            self.a == other.a and
            self.b == other.b and
            self.c == other.c and
            self.d == other.d and
            self.e == other.e
        )
        return truthiness

    def __dict__(self):
        return dict(a=self.a, b=self.b, c=self.c, d=self.d, e=self.e)

    def to_json(self):
        return json.dumps(self.__dict__(), ensure_ascii=False)

class MessageTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

class MessageTestSuite(MessageTest):
    # Unique IDs
    def test_unique_ids(self):
        """Messages created all have a unique ID"""
        ids = set()
        num_messages = 1000
        for _ in range(num_messages):
            message = Message()
            ids.add(message.id)

        self.assertEqual(len(ids), num_messages)

    def test_command_message_serialize(self):
        """CommandMessage serialize method works"""
        intent = "COMMAND"

        filter = "10000"
        id = "1"
        app_name = "testing_app"
        version = "0.0.1"
        command = "TEST"

        in_args = [filter, id, app_name, version, intent, command]
        command_message = CommandMessage(
            filter=filter,
            id=id,
            app_name=app_name,
            version=version,
            command=command
        )

        serialized = command_message.serialize()
        out_args = serialized.split(DELIMITER)

        self.assertEqual(in_args, out_args)

    def test_document_message_serialize(self):
        """DocumentMessage serialize method works"""
        intent = "DOCUMENT"

        filter = "10000"
        id = "1"
        app_name = "testing_app"
        version = "0.0.1"
        document = "{\"test_struct\":{\"data\"=\"fake\"}}"

        in_args = [filter, id, app_name, version, intent, document]
        document_message = DocumentMessage(
            filter=filter,
            id=id,
            app_name=app_name,
            version=version,
            document=document
        )
        serialized = document_message.serialize()
        out_args = serialized.split(DELIMITER)

        self.assertEqual(in_args, out_args)

    def test_command_message_construction_via_deserialize0(self):
        """CommandMessage deserialize constructor works (with filter)"""
        filter = "10000"
        id = "123456"
        app_name = "testing_app"
        version = "0.0.1.1.1.2"
        intent = "COMMAND"
        command = "PERFORM_TEST"
        in_args = [filter, id, app_name, version, intent, command]

        message_string = "{}"
        message_string = message_string + (DELIMITER+"{}")*5
        message_string = message_string.format(
            filter,
            id,
            app_name,
            version,
            intent,
            command
        )

        command_message = CommandMessage.deserialize(message_string)
        out_args = [
            command_message.filter,
            command_message.id,
            command_message.app_name,
            command_message.version,
            command_message.intent,
            command_message.contents
        ]
        self.assertEqual(in_args, out_args)

    def test_command_message_construction_via_deserialize1(self):
        """CommandMessage deserialize constructor works (without filter)"""
        id = "123456"
        app_name = "testing_app"
        version = "0.0.1.1.1.2"
        intent = "COMMAND"
        command = "PERFORM_TEST"
        in_args = [id, app_name, version, intent, command]

        message_string = "{}"
        message_string = message_string + (DELIMITER+"{}")*4
        message_string = message_string.format(
            id,
            app_name,
            version,
            intent,
            command
        )

        command_message = CommandMessage.deserialize(message_string)
        out_args = [
            command_message.id,
            command_message.app_name,
            command_message.version,
            command_message.intent,
            command_message.contents
        ]
        self.assertEqual(in_args, out_args)

    def test_document_message_construction_via_deserialize0(self):
        """DocumentMessage deserialize constructor works (with filter)"""
        filter = "10000"
        id = "123456"
        app_name = "testing_app"
        version = "0.0.1.1.1.2"
        intent = "DOCUMENT"
        document = "{\"test_struct\":{\"data\"=\"fake\"}}"
        in_args = [filter, id, app_name, version, intent, document]

        message_string = "{}"
        message_string = message_string + (DELIMITER+"{}")*5
        message_string = message_string.format(
            filter,
            id,
            app_name,
            version,
            intent,
            document
        )

        document_message = DocumentMessage.deserialize(message_string)
        out_args = [
            document_message.filter,
            document_message.id,
            document_message.app_name,
            document_message.version,
            document_message.intent,
            document_message.contents
        ]
        self.assertEqual(in_args, out_args)

    def test_document_message_construction_via_deserialize1(self):
        """DocumentMessage deserialize constructor works (without filter)"""
        id = "123456"
        app_name = "testing_app"
        version = "0.0.1.1.1.2"
        intent = "DOCUMENT"
        document = "{\"test_struct\":{\"data\"=\"fake\"}}"
        in_args = [id, app_name, version, intent, document]

        message_string = "{}"
        message_string = message_string + (DELIMITER+"{}")*4
        message_string = message_string.format(
            id,
            app_name,
            version,
            intent,
            document
        )

        document_message = DocumentMessage.deserialize(message_string)
        out_args = [
            document_message.id,
            document_message.app_name,
            document_message.version,
            document_message.intent,
            document_message.contents
        ]
        self.assertEqual(in_args, out_args)

    def test_command_message_deconstruction_reconstruction0(self):
        """CommandMessage survives serialization and deserialization (filter)"""
        original_message = CommandMessage(
            filter="10001",
            id="1a2b3c4d",
            app_name="test_app",
            version="10.0.1.101.12301",
            command="TESTINSHIT"
        )

        serialized = original_message.serialize()
        deserialized_message = CommandMessage.deserialize(serialized)

        self.assertEqual(original_message, deserialized_message)

    def test_command_message_deconstruction_reconstruction1(self):
        """CommandMessage survives serialization and deserialization (no filter)"""
        original_message = CommandMessage(
            id="1a2b3c4d",
            app_name="test_app",
            version="10.0.1.101.12301",
            command="TESTINSHIT"
        )

        serialized = original_message.serialize()
        deserialized_message = CommandMessage.deserialize(serialized)

        self.assertEqual(original_message, deserialized_message)

    def test_document_message_deconstruction_reconstruction(self):
        """DocumentMessage survives serialization/deserialization (filter)"""
        original_message = DocumentMessage(
            filter="12319240124",
            id="9z8x7y6w",
            app_name="test_app",
            version="2130123.231.31494251",
            document="{\"test_struct\":{\"data\"=\"fake\"}}"
        )

        serialized = original_message.serialize()
        deserialized_message = DocumentMessage.deserialize(serialized)

        self.assertEqual(original_message, deserialized_message)

    def test_document_message_deconstruction_reconstruction(self):
        """DocumentMessage survives serialization/deserialization (no filter)"""
        original_message = DocumentMessage(
            id="9z8x7y6w",
            app_name="test_app",
            version="2130123.231.31494251",
            document="{\"test_struct\":{\"data\"=\"fake\"}}"
        )

        serialized = original_message.serialize()
        deserialized_message = DocumentMessage.deserialize(serialized)

        self.assertEqual(original_message, deserialized_message)

    def test_command_message_reply_construction(self):
        """CommandMessage reply correlates with original message"""
        test_id = "1000"
        app_name = "testing_app"
        version = "102013921"
        command = "TESTINGSTUFF"
        request_message = CommandMessage(
            id=test_id,
            app_name=app_name,
            version=version,
            command=command
        )

        reply_message = CommandMessage.Reply(request_message, "OK")
        self.assertTrue(reply_message.correlates_with(request_message))

    def test_command_message_void_reply_construction(self):
        """CommandMessage void reply's contents are empty"""
        test_id = "1000"
        app_name = "testing_app"
        version = "102013921"
        command = "TESTINGSTUFF"
        request_message = CommandMessage(
            id=test_id,
            app_name=app_name,
            version=version,
            command=command
        )

        void_reply_message = CommandMessage.VoidReply(request_message)
        self.assertEqual(void_reply_message.contents, '')

    def test_document_message_reply_construction(self):
        """DocumentMessage reply correlates with original message"""
        test_id = "1000"
        app_name = "testing_app"
        version = "102013921"
        document = "{\"test_struct\":{\"data\"=\"fake\"}}"
        request_message = DocumentMessage(
            id=test_id,
            app_name=app_name,
            version=version,
            document=document
        )

        reply_message = DocumentMessage.Reply(
            request_message,
            "{\"test_struct\":{\"reply\"=\"fanfuckingtastic\"}}"
        )
        self.assertTrue(reply_message.correlates_with(request_message))

    def test_document_message_void_reply_construction(self):
        """DocumentMessage void reply's contents are empty"""
        test_id = "1000"
        app_name = "testing_app"
        version = "102013921"
        document = "{\"test_struct\":{\"data\"=\"fake\"}}"
        request_message = DocumentMessage(
            id=test_id,
            app_name=app_name,
            version=version,
            document=document
        )

        reply_message = DocumentMessage.VoidReply(request_message)
        self.assertEqual(reply_message.contents, '')

    def test_struct_reconstruction(self):
        """Message's serialize/deserialize methods on TestStruct returns original"""
        test_object = TestStruct(
            102130943,
            12.3240193,
            "This is a cool struct",
            True,
            1230914
        )

        test_id = "10000"
        app_name = "testing_app"
        version = "1231094416"
        document = test_object.to_json()

        message = DocumentMessage(
            id=test_id,
            app_name=app_name,
            version=version,
            document=document
        )

        serialized = message.serialize()
        new_message = DocumentMessage.deserialize(serialized)
        new_document = new_message.document
        reconstructed_test_object = TestStruct.from_json(new_document)

        self.assertEqual(test_object, reconstructed_test_object)
