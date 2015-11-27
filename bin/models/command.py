from enum import Enum

class Command(Enum):
    STATUS = 'STATUS'
    VOID = 'VOID'
    SHUTDOWN = 'SHUTDOWN'

    def serialize(self):
        return self.value

    @classmethod
    def deserialize(cls, string):
        return cls(string)
