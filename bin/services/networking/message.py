import uuid, re

from bin import APP_NAME, VERSION

DELIMITER = ' | '

def NEW_ID():
    id = uuid.uuid4()

    return id.hex

class Message:
    @classmethod
    def Reply(
            cls,
            request,
            contents
    ):
        return cls(
            filter=request.filter,
            id=request.id,
            app_name=request.app_name,
            version=request.version,
            contents=contents
        )

    @classmethod
    def VoidReply(cls, request):
        return cls(
            id=request.id,
            app_name=request.app_name,
            version=request.version,
            contents=''
        )

    @classmethod
    def deserialize(cls, message_string):
        # assumes message is formatted properly
        # raise TypeError(message_string.split(DELIMITER))
        args = message_string.split(DELIMITER)
        if len(args) == 6:
            filter, id, app_name, version, intent, contents = args
        else:
            filter = None
            id, app_name, version, intent, contents = args

        return cls(
            filter=filter,
            id=id,
            app_name=app_name,
            version=version,
            intent=intent,
            contents=contents
        )

    def __init__(
            self,
            filter=None,
            id=None,
            app_name=APP_NAME,
            version=VERSION,
            intent="",
            contents=None
    ):
        self.filter = filter
        self.id = id if id else NEW_ID()
        self.app_name = app_name
        self.version = version
        self.intent = intent
        self.contents = contents

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        truthiness = (
            self.filter == other.filter and
            self.id == other.id and
            self.app_name == other.app_name and
            self.version == other.version and
            self.intent == other.intent and
            self.contents == other.contents
        )
        return truthiness

    def serialize(self):
        f = '{}'.format(self.filter) if self.filter else ''
        if f: f = f+DELIMITER
        string = f+(
            '{}'+DELIMITER+
            '{}'+DELIMITER+
            '{}'+DELIMITER+
            '{}'+DELIMITER+
            '{}'
        )

        string = string.format(
            self.id,
            self.app_name,
            self.version,
            self.intent,
            self.contents
        )
        return string

    def correlates_with(self, other):
        return self.id == other.id

class CommandMessage(Message):
    def __init__(
            self,
            filter=None,
            id=None,
            app_name=APP_NAME,
            version=VERSION,
            intent="COMMAND",
            command="",
            contents="" # allows for inherited factory
    ):
        super().__init__(
            filter=filter,
            id=id,
            app_name=app_name,
            version=version,
            intent=intent,
            contents=command or contents # allows for inherited factory
        )
        self.command = command or contents

class DocumentMessage(Message):
    _intent = "DOCUMENT"
    def __init__(
            self,
            filter=None,
            id=None,
            app_name=APP_NAME,
            version=VERSION,
            intent="DOCUMENT",
            document="",
            contents="" # allows for inherited factory
    ):
        super().__init__(
            filter=filter,
            id=id,
            app_name=app_name,
            version=version,
            intent=intent,
            contents=document or contents
        )
        self.document = document or contents
