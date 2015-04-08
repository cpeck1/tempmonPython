import usb.core # pyusb
import usb1 # libusb1
import pyudev # duh

from bin.models.singleton import Singleton

from bin.services.usb_library_translator import (
    PyudevDevice,
    Libusb1Device,
    PyusbDevice
)
from bin.services.hex_zpadded import hex_zpadded

from bin.models.exceptions import (
    UnsupportedUsbLibraryError, 
    InvalidDeviceError
)

@Singleton
class UsbBus:
    def __init__(self):
        self.devices = []
            
    def add(self, device):
        """
        add the device to the usb bus, unless it is not a UsbDevice
        or is already present in the usb bus
        """
        if not isinstance(device, UsbDevice):
            raise InvalidDeviceError
        
        if self.find(device) is None:
            self.devices.append(device)

    def find(self, device):
        """
        return the index that device appears at within the bus, or 
        none if the device is not in the bus
        """
        for index, dev in enumerate(self.devices):
            if dev == device:
                return index
        return None

    def find_with(self, **attributes):
        for device in self.devices:
            match = True
            try:
                for att_name, att_val in attributes.items():
                    device_att_val = getattr(device, att_name) 
                    match = match and (device_att_val == att_val)
            except KeyError as e:
                return
            if match:
                return device

class UsbDevice:
    """A USB device with attribute naming conventions similar to the 
    Linux command lsusb

    The wrapper class for usb devices used on this system. All relevant
    information will be available within one of these devices, and all 
    the irrelevant stuff like interfaces, endpoints, descriptors etc 
    will not. Necessitated by the variety of usb device representations
    used by the packages within this system and the fact that they ALL 
    use different naming schemes for attributes. Constructing a device
    from certain USB device classes will require OTHER USB device 
    classes to determine every attribute (for example pyusb does not 
    support determining system device paths and pyudev does not support
    (properly) determining port numbers)
    """
    def __init__(self, device):
        """
        We need to find the corresponding device in both the pyudev
        and the libusb1 library. Between the two we can gather all
        the information we need about the device and combine it 
        together into a unified whole. Start by finding the pyusb
        equivalent of the given device 
        """
        pyudev_device = None
        if isinstance(device, pyudev.device.Device):
            pyudev_device = PyudevDevice(device)
        elif isinstance(device, usb1.USBDevice):
            pyudev_device = PyudevDevice.find_using_device(
                Libusb1Device(device)
            ) 
        elif isinstance(device, usb.core.Device):
            pyudev_device = PyudevDevice.find_using_device(
                PyusbDevice(device)
            )
        else:
            raise UnsupportedUsbLibraryError

        if pyudev_device is None: raise InvalidDeviceError

        self.path = pyudev_device.path
        self.bus = pyudev_device.bus
        self.device = pyudev_device.device
        self.idVendor = pyudev_device.idVendor
        self.idProduct = pyudev_device.idProduct
        self.manufacturer = pyudev_device.manufacturer
        self.product = pyudev_device.product

        # now we need the libusb1 equivalent in order to determine the 
        # device path
        libusb_device = Libusb1Device.find_using_device(pyudev_device)
        self.port = libusb_device.port

    def __eq__(self, other):
        if isinstance(other, type(self)): 
            return (
                # these attributes guarantee uniqueness within the 
                # system
                self.path == other.path and
                self.bus == other.bus and
                self.device == other.device and
                self.idVendor == other.idVendor and
                self.idProduct == other.idProduct
            )
        else:
            return False

    def __repr__(self):
        return "UsbDevice(path={}, bus={}, device={}, idVendor={}, idProduct={}, manufacturer={}, product={})".format(
            self.path,
            self.bus,
            self.device,
            hex_zpadded(self.idVendor, 4),
            hex_zpadded(self.idProduct, 4),
            self.manufacturer,
            self.product
        )
