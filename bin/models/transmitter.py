class Transmitter:
    """
    represents a temperature transmitter with a USB interface
    """
    def __init__(
            self, container_id, manufacturer=None, 
            name=None, vendor_id=None, product_id=None):
        assert (isinstance(container_id, int))
    
        self._container_id = container_id
        self._manufacturer = None
        self._name = None
        self._vendor_id = None
        self._product_id = None

        self._device = None

        self._open_method = None
        self._close_method = None
        self._read_method = None

        if manufacturer:
            self.manufacturer = manufacturer
        if name:
            self.name = name
        if vendor_id:
            self.vendor_id = vendor_id
        if product_id:
            self.product_id = product_id
            
    @property
    def container_id(self):
        """
        return this transmitter's container id
        
        Usage:
        >>> trans = Transmitter(12345)
        >>> trans.container_id
        12345
        """
        return self._container_id

    @property
    def manufacturer(self):
        """
        return this transmitter's manufacturer name
        
        Usage:
        >>> trans = Transmitter(12345, manufacturer="test")
        >>> trans.manufacturer
        'test'
        """
        return self._manufacturer
    
    @manufacturer.setter
    def manufacturer(self, manufacturer):
        """
        set this transmitter's manufacturer name. 

        *** manufacturer must be of type string ***

        Usage:
        >>> trans = Transmitter(12345, manufacturer="test1")
        >>> self.manufacturer = "test2"
        >>> self.manufacturer
        'test2'

        >>> self.manufacturer = 12345
        Traceback (most recent call last):
        ...
        AssertionError: expected <type 'str'> but got <type 'int>
        """
        assert isinstance(manufacturer, str), \
            "expected <type 'str'> but got " + str(type(manufacturer))
    
        self._manufacturer = manufacturer

    @property
    def name(self):
        """
        return this transmitter's name

        Usage:
        >>> trans = Transmitter(12345, name="test")
        >>> trans.name
        'test'
        """
        return self._name
    
    @name.setter
    def name(self, name):
        """
        set this transmitter's name

        *** name must be of type str ***

        Usage:
        >>> trans = Transmitter(12345, "test1")
        >>> trans.name = "test2"
        >>> trans.name
        'test2'

        >>> trans.name = 12345
        Traceback (most recent call last):
        ...
        AssertionError: expected <type 'str'> but got <type 'int'>
        """
        assert isinstance(name, str), \
            "expected <type 'str'> but got " + str(type(name))

        self._name = name

    @property
    def vendor_id(self):
        """
        return this transmitter's vendor id 

        Usage:
        >>> trans = Transmitter(12345, vendor_id=0x1230)
        >>> hex(trans.vendor_id)
        '0x1230'
        """
        return self._vendor_id

    @vendor_id.setter
    def vendor_id(self, vId):
        """
        set this transmitter's vendor id
        
        *** vId must be of type int ***
        *** vId must fall in the range (inclusive) [0x0001, 0xFFFF]

        Usage:
        >>> trans = Transmitter(12345, vendor_id=0x4501)
        >>> vId = 0x1234
        >>> trans.vendor_id = vId
        >>> hex(trans.vendor_id)
        '0x1234'

        >>> trans.vendor_id = 0.1234
        Traceback (most recent call last):
        ...
        AssertionError: expected <type 'int'> but got <type 'float'>

        >>> trans.vendor_id = 0x0000
        Traceback (most recent call last):
        ...
        AssertionError: given id 0x0 out of range [0x0001, 0xFFFF]
        """
        assert isinstance(vId, int), \
            "expected <type 'int'> but got " + str(type(vId))

        # note that the upper bound on range is EXCLUSIVE hence the 0x10000
        assert vId in range(0x0001, 0x10000), \
            "given id " + hex(vId) + " out of range [0x0001, 0xFFFF]"

        self._vendor_id = vId

    @property
    def product_id(self):
        """
        return this transmitter's product id

        Usage:
        >>> trans = Transmitter(12345, product_id=0x1234)
        >>> hex(trans.product_id)
        '0x1234'
        """
        return self._product_id

    @product_id.setter
    def product_id(self, pId):
        """
        set this transmitter's product id

        *** pId must be of type int ***
        *** pId must be within the range (inclusive) [0x0001, 0xFFFF]
        
        Usage:
        >>> trans = Transmitter(12345, product_id=0x1234)
        >>> trans.product_id = 0x4321
        >>> hex(trans.product_id)
        '0x4321'

        >>> trans.product_id = 0.1234
        Traceback (most recent call last):
        ...
        AssertionError: expected <type 'int'> but got <type 'float'>
        
        >>> trans.product_id = 0x10000
        Traceback (most recent call last):
        ...
        AssertionError: given id 0x10000 out of range [0x0001, 0xFFFF]
        """
        assert isinstance(pId, int), \
            "expected <type 'int'> but got " + str(type(pId))

        # note that the upper bound on range is EXCLUSIVE hence the 0x10000
        assert pId in range(0x0001, 0x10000), \
            "given id " + str(pId) + " out of range [0x0001, 0xFFFF]"

        self._product_id = pId

    def vid_pid_valid(self):
        """
        returns whether vid and pid are int instances, both within the range
        [0x0000, 0xFFFF]

        Usage:
        >>> trans = Transmitter(12345, vendor_id=0x1234, product_id=0x4321)
        >>> assert trans.vid_pid_valid()
        """
        vid = self.vendor_id
        pid = self.product_id

        return (isinstance(vid, int) and
                isinstance(pid, int) and
                (vid in range(0x0001, 0x10000)) and
                (pid in range(0x0001, 0x10000)))

    def method_available(self, method_str):
        """
        returns whether this transmitter has the given method available. The 
        given method must be a string, of value:
            'open' - checks whether this transmitter has an open method 
            'read' - checks whether this transmitter has a read method
            'close' - checks whether this transmitter has a close method
        any other string passed returns False.

        Usage:
        >>> trans = Transmitter(12345)
        >>> trans.method_available('open')
        False
        >>> trans.set_open_method(print)
        >>> trans.method_available('open')
        True

        >>> trans.set_read_method(lambda x: x)
        >>> trans.method_available('read')
        True
    
        >>> trans.set_close_method(lambda x: None)
        >>> trans.method_available('close')
        True

        >>> trans.method_available('bizzare request')
        False
        """
        return {
            'open': hasattr(self._open_method, '__call__'),
            'read': hasattr(self._read_method, '__call__'),
            'close': hasattr(self._close_method, '__call__')
        }.get(method_str, False)

    def open(self):
        """
        invoke this transmitter's open method; if set properly, should open the
        USB device with the vendor id and product id held by this transmitter.
        Note this does not return the device, rather it assigns it to this 
        transmitter's _device attribute

        Case 0: there is no method assigned to this transmitter's open method,
        Result: raise exception

        Case 0.1: this transmitter's properties are insufficient for opening a
        device
        Result: raise exception

        Case 1: there is no USB device attached with the vendor and product ID
        given by this device.
        Result: return immediately

        Case 2: there is a USB device attached with that vendor and product ID,
        but the device is busy
        Result: return immediately

        Case 3: the open method successfully opens the device
        Result: the device is placed in this transmitter's device attribute and
        the function returns (nothing)

        Case 4: this transmitter is already open
        Result: return immediately
        
        Usage:
        >>> trans = Transmitter(12345)
        >>> trans.open() 
        Traceback (most recent call last):
        ...
        AssertionError: insufficient properties to complete transaction
        
        >>> trans.vendor_id = 0x0001
        >>> trans.product_id = 0x0001
        >>> trans.open()
        Traceback (most recent call last):
        ...
        AssertionError: no open method assigned

        >>> trans.set_open_method(lambda x,y: x+y)
        >>> trans.open() # do stuff with device

        >>> trans.open() # device already open, but no exception raised
        """
        assert self.vid_pid_valid(),\
            "insufficient properties to complete transaction"

        assert self.method_available('open'),\
            "no open method assigned"        
        
        if not self.is_open():
            self._device = self._open_method(self.vendor_id, self.product_id)

    def set_open_method(self, method):
        """
        set this transmitter's open method, which takes a vendor id and product 
        id as arguments

        *** method must be callable ***

        Usage:
        >>> trans = Transmitter(12345)
        >>> trans.vendor_id = 0x0001
        >>> trans.product_id = 0x0001
        
        >>> trans.set_open_method(1)
        Traceback (most recent call last):
        ...
        AssertionError: method must be callable

        >>> om = lambda x, y: x+y
        >>> trans.set_open_method(om)
        >>> trans.open()
        >>> trans._device
        2
        """
        # TODO: move this to a 'callable' method in some external service
        assert hasattr(method, '__call__'),\
            "method must be callable"
    
        self._open_method = method 

    def is_open(self):
        """
        return whether this transmitter is open, i.e. the open() function has
        successfully been called

        Usage:
        >>> trans = Transmitter(12345, "Man1", "Name1", 1, 1)
        >>> trans.is_open()
        False

        >>> trans.set_open_method(lambda x, y: x+y)
        >>> trans.open()
        >>> trans.is_open()
        True
        """
        return self._device is not None

    def read(self):
        """
        invoke this transmitter's read method; if set properly, should read the
        USB device that must be already opened within this transmitter.
        
        returns the reading gathered from the device

        Case 0: there is no method assigned to this transmitter's read method,
        Result: raise exception

        Case 1: this transmitter's properties are insufficient for reading the
        device (for instance if missing a device to read altogether
        Result: raise exception

        Case 2: there is a USB device attached with that vendor and product ID,
        but the device cannot be read
        Result: return immediately

        Case 3: the open method successfully reads the device
        Result: returns the reading

        Case 4: the reading fails
        Result: returns immediately

        Usage:
        >>> trans = Transmitter(12345, "Man1", "Name1", 1, 1)
        >>> trans.set_open_method(lambda x, y: x + y)
        >>> trans.open()
        
        >>> trans.read()
        Traceback (most recent call last):
        ...
        AssertionError: no read method assigned

        >>> trans.set_read_method(lambda x: x)
        >>> trans.read() # note this just returns the _device property
        2
        """
        assert self.method_available('read'),\
            "no read method assigned"
        
        assert self.vid_pid_valid(),\
            "insufficient properties to complete transaction"

        assert self.is_open(),\
            "device must be open in order to read"

        return self._read_method(self._device)
        

    def set_read_method(self, method):
        """
        sets this device's read method, which takes a device to read as an 
        argument

        *** method must be callable ***

        Usage:
        >>> trans = Transmitter(12345, "Man1", "Name1", 1, 1)
        >>> trans.set_read_method(1)
        Traceback (most recent call last):
        ...
        AssertionError: method must be callable

        >>> rm = lambda x: x
        >>> trans.set_read_method(rm)
        """
        assert hasattr(method, '__call__'),\
            "method must be callable"
    
        self._read_method = method 

    def close(self):
        """
        invoke this transmitter's close method; if set properly, should close 
        the USB device
        
        Case 0: there is no method assigned to this transmitter's close method,
        Result: exception raised

        Case 1: this transmitter's properties are insufficient for closing the
        device (for instance if missing a device to read altogether
        Result: exception raised

        Case 2: there is no USB device to close.
        Result: returns immediately

        Case 3: the open method successfully reads the device
        Result: returns the reading

        Case 4: closing device fails
        Result: returns immediately

        Usage:
        >>> trans = Transmitter(12345, "Man1", "Name1", 1, 1)

        >>> trans.set_open_method(lambda x, y: x+y)
        >>> trans.set_close_method(lambda x: x)

        >>> trans.close() # device not opened yet
        >>> trans.open() 

        >>> trans.close() # device now open, call close method

        >>> trans.close() # device already closed, returns nothing
        """
        assert self.method_available('close'),\
            "no close method assigned"

        if (self.is_open()):
            self._close_method(self._device)

        self._device = None

    def set_close_method(self, method):
        """
        sets this device's close method, which takes a device to close as an 
        argument

        *** method must be callable ***
        
        >>> trans = Transmitter(12345, "Man1", "Name1", 1, 1)        
        >>> trans.set_close_method(1)
        Traceback (most recent call last):
        ...
        AssertionError: method must be callable

        >>> trans.set_close_method(print)
        """
        assert hasattr(method, '__call__'),\
            "method must be callable"

        self._close_method = method

if __name__ == "__main__": 
    import doctest
    doctest.testmod()
