class AlarmInactiveException(Exception):
    pass

class UnsupportedUsbLibraryError(Exception):
    pass

class DeviceNotFoundError(Exception):
    pass

class InvalidDeviceError(Exception):
    pass

class InvalidReadMethodError(Exception):
    pass

class NoDeviceHandleError(Exception):
    pass

class NoChannelNumberError(Exception):
    pass
