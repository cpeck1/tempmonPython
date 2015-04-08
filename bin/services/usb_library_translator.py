import usb.core
import usb1
import pyudev

try:
    from .hex_manipulation import int_base_16
except SystemError:
    from hex_manipulation import int_base_16

class UsbLibraryDeviceWrapper:
    """Wraps a USB device given in a USB library in order to provide the
    same interface to all forms of USB devices available in different
    libraries. Attributes are as unified as possible across libraries, 
    conforming to the standard set in the linux command lsusb. Note 
    however that different libraries offer different attributes and some
    forms of USB devices do not offer methods to retrieve certain 
    attributes
    """
    _device_list = []

    @classmethod
    def get_device_list(cls):
        """
        --- THIS METHOD MUST BE OVERRIDDEN --- 
        Returns the USB device list for this particular library
        """
        # Trick to guarantee override:
        assert (1 == 0), cls.get_device_list.__doc__
        
    @classmethod
    def refresh_device_list(cls):
        """
        Refresh the list of devices this class refers to
        """
        cls._device_list = []
        dev_list = cls.get_device_list()
        for device in dev_list:
            cls._device_list.append(cls(device))

    @classmethod
    def find_using_device(cls, other_device):
        """Return the device in this representation by finding the 
        match to the given other_device within this library's device 
        list. 

        Note that a USB device is unique up to its bus, device, and 
        vendor and product IDs (i.e. no two device can have the same
        bus number, device number and vendor and product IDs on a 
        system, although individually they may have matches within the
        system) and therefore this function uses find_using_attributes 
        with these attributes to find a match.
        """
        return cls.find_using_attributes(
            bus=other_device.bus,
            device=other_device.device,
            idVendor=other_device.idVendor,
            idProduct=other_device.idProduct
        )

    @classmethod
    def find_using_attributes(cls, **attributes):
        """Return the first device in this representation whose 
        attributes match those given. 

        This function searches the device list given by this library's
        "find all devices" function.
        """
        cls.refresh_device_list()
        for device in cls._device_list:
            match = True 
            try:
                for att_name, att_val in attributes.items():
                    device_att_val = getattr(device, att_name) 
                    match = match and (device_att_val == att_val)
                    if not match:
                        # match will never be True again
                        continue
            except KeyError as e:
                match = False
            if match:
                return device

    def __init__(self, device):
        """
        create a device from the same device in a different 
        representation
        """
        self.wrapped = device

    def _get_attribute(self, attr):
        """
        --- THIS METHOD MUST BE OVERRIDDEN ---
        Return the value of the given attribute or None 
        """
        assert (1 != 0), self._get_attribute.__doc__

    def __getattr__(self, attr):
        """Get the given attribute from the wrapped usb class

        raises AttributeError if the attribute is not found
        """
        ret = self._get_attribute(attr)
        
        if ret is not None: return ret
        
        raise AttributeError(
            "'{}' object has no attribute '{}'".format(
                type(self), 
                attr
            )
        )        

class PyudevDevice(UsbLibraryDeviceWrapper):
    """
    wrapper for pyudev.device.Device object

    Available attributes:
    bus          - bus number of the system the device occupies
    device       - device number assigned to the device by the system
    idVendor     - ID of the manufacturer of the device
    idProduct    - Product ID of the device
    product      - name of the product (if available)
    manufacturer - name of the manufacturer (if available)
    path         - path to the device on the system
    """
    @classmethod
    def get_device_list(cls):
        """the method the pyudev library uses to get the list of USB
        devices on the system
        """
        usb_related_devices = pyudev.Context().list_devices(subsystem='usb')
        return [
            device for device in usb_related_devices if (
                device.device_type=='usb_device'
            )
        ]

    def _attribute_map(self, attr):
        """
        maps the given attribute to the udev attribute, the 
        function needed to convert it and the default value
        in the event of a keyerror or other exception; 
        
        leaving it as a triple because it's an internal function
        not intended to be used elsewhere, but for future 
        developers just remember: 
        ("attribute name", conversion_function, default_value) 
        """
        return {
            "bus":          ("busnum", int, -1),
            "device":       ("devnum", int, -1),
            "idVendor":     ("idVendor", int_base_16, -1),
            "idProduct":    ("idProduct", int_base_16, -1),
            "product":      ("product", str, "Not Specified"),
            "manufacturer": ("manufacturer", str, "Not Specified"),
            "path":         ("path", str, "")
        }.get(attr, None)
        

    def _get_attribute(self, attr):
        """
        Return the value of the given attribute or None
        """
        attr_mapped = self._attribute_map(attr)

        if attr_mapped is None: return None
        elif attr_mapped[0] == "path":
            # special case: the attribute is path in which case we don't 
            # query the device's attributes 
            try:
                return self.wrapped.device_path
            except: # not sure what pyudev raises when this fails
                return attr_mapped[2]
        else:
            try:
                # remember attr_mapped[1] is the conversion function
                return attr_mapped[1](
                    # note all pyudev attributes are given as bytes so 
                    # they need to be decoded into strings first
                    self.wrapped.attributes[attr_mapped[0]].decode('utf-8')
                )
            except KeyError:
                # pyudev doesn't have default values when a device 
                # doesn't have a certain attribute, it just raises a key
                # error when absent. This, in my opinion, is horrible 
                # behaviour (why would two USB devices in the system 
                # have different sets of available attributes? that's 
                # crazy talk) so default values are provided
                return attr_mapped[2]
            
class Libusb1Device(UsbLibraryDeviceWrapper):
    """
    wrapper for pyudev.device.Device object

    Available attributes:
    bus          - bus number of the system the device occupies
    device       - device number assigned to the device by the system
    idVendor     - ID of the manufacturer of the device
    idProduct    - Product ID of the device
    port         - physical port numbers of the device
    """
    @classmethod
    def get_device_list(cls):
        return usb1.USBContext().getDeviceList()

    def _get_attribute(self, attr):
        """
        Return the value of the given attribute or None

        methods for getProduct and get Manufacturer are available but
        don't work most of the time, so they are excluded
        """ 
        return {
            # these attributes haven't raised errors and have always 
            # returned appropriate values in my experience, but it's 
            # entirely possible this isn't always the case.
            'bus': self.wrapped.getBusNumber(),
            'device': self.wrapped.getDeviceAddress(),
            'idVendor': self.wrapped.getVendorID(),
            'idProduct': self.wrapped.getProductID(), 
            'port': self.wrapped.getPortNumberList()
        }.get(attr, None)

class PyusbDevice(UsbLibraryDeviceWrapper):
    """
    wrapper for pyudev.device.Device object

    Available attributes:
    bus          - bus number of the system the device occupies
    device       - device number assigned to the device by the system
    idVendor     - ID of the manufacturer of the device
    idProduct    - Product ID of the device
    """
    @classmethod
    def get_device_list(cls):
        return usb.core.find(find_all=True)

    def _get_attribute(self, attr):
        """
        Return the value of the given attribute or None

        attributes for product and manufacturer are available, but they
        don't work most of the time so they are excluded
        """
        return {
            'bus': self.wrapped.bus,
            'device': self.wrapped.address,
            'idVendor': self.wrapped.idVendor,
            'idProduct': self.wrapped.idProduct 
        }.get(attr, None)
