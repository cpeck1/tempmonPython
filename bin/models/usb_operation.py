import json
from bin.infrastructure.usb_bus import UsbDevice
from bin.infrastructure.operation import Operation

class UsbOperation:
    """
    Convenience object for messaging between the USB monitor and
    transmitter application controllers.
    """
    @classmethod
    def from_json(cls, json_obj):
        if type(json_obj) == str:
            dct = json.loads(json_obj)
        elif type(json_obj) == dict:
            dct = json_obj

        return cls(
            operation=Operation.from_json(dct['operation']),
            usb_device=UsbDevice.from_json(dct['usb_device'])
        )

    def __init__(self, operation, usb_device):
        self.operation = operation
        self.usb_device = usb_device

    def __repr__(self):
        return "Operation(usb_device={}, operation={})".format(
            repr(self.usb_device),
            repr(self.operation)
        )

    def __eq__(self, other):
        try:
            return (
                self.usb_device == other.usb_device and
                self.operation == other.operation
            )
        except AttributeError:
            return False

    def __dict__(self):
        return dict(operation=self.operation, usb_device=self.usb_device)

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__()
        )
