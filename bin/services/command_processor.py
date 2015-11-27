from bin.models.command import Command
from bin.models.exceptions import ExitProcess

class CommandProcessor:
    """
    command processing unit
    """
    @classmethod
    def __init__(self, obj):
        self.obj = obj

    def process(self, command):
        if command is Command.STATUS:
            return self.obj.to_json()
        elif command is Command.VOID:
            return
        elif command is Command.SHUTDOWN:
            raise ExitProcess
