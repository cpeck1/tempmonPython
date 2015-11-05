import json
from bin.infrastructure.usb_bus import UsbDevice

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
            usb_device=UsbDevice.from_json(dct['usb_device']),
            operation=dct['operation']
        )

    def __init__(self, usb_device, operation):
        self.usb_device = usb_device
        self.operation = operation

    def __dict__(self):
        return dict(usb_device=self.usb_device, operation=self.operation)

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
        except TypeError:
            return False

    def to_json(self):
        return json.dumps(
            self.__dict__(),
            default=lambda o: o.__dict__()
        )
