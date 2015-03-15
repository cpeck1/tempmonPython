class AlarmInactiveException(Exception):
    """
    Invoked when an alarm that is no longer active is ended
    """
    pass

class InvalidReadMethod(Exception):
    """
    Invoked when a channel is read with a read method that is 
    not callable
    """
    pass

class NoDeviceHandle(Exception):
    """
    Invoked when a channel is read but it doesn't have a device handle
    """
    pass

class NoChannelNumber(Exception):
    """
    Invoked when a channel is read but it didn't receive a channel 
    number from its transmitter
    """
