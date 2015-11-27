import json
from enum import Enum

class Operation(Enum):
    """
    Possible event actions produced by pyudev when something about a USB
    device changes on the system
    """
    ADD = 'add'
    REMOVE = 'remove'
    CHANGE = 'change'
    ONLINE = 'online'
    OFFLINE = 'offline'

    def serialize(self):
        return self.value

    @classmethod
    def deserialize(cls, string):
        return cls(string)

    @classmethod
    def from_json(cls, json_obj):
        if type(json_obj) == str:
            dct = json.loads(json_obj)
        elif type(json_obj) == dict:
            dct = json_obj

        return cls(value=dct['value'])

    def __dict__(self):
        return dict(value=self.value)
