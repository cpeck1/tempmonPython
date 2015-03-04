import os
import importlib.machinery
from ..models.transmitter import Transmitter

directory = "./transmitters"
transmitter_file_name = "usbinfo.py"

# sort of a case class, shell for holding a few pieces of data
class _TransmitterIdent:
    def __init__(
            self, 
            manufacturer, 
            name, 
            vendor_id,
            product_id, 
            channel_units,
            open_method,
            read_channel_method,
            close_method
    ):
        self.manufacturer = manufacturer
        self.name = name
        self.vendor_id = vendor_id
        self.product_id = product_id
        
        self.channel_units = channel_units

        self.open_method = open_method,
        self.read_channel_method = read_channel_method,
        self.close_method = close_method

    def matches(self, vid, pid):
        return ((self.idVendor == vid) and (self.idProduct == pid))

class _TransmitterCache:
    """
    cache of transmitters from the transmitter package based on
    the transmitter_file_name modules inside, which contain the 
    manufacturer, name, product and vendor ids of each transmitter 
    within the system
    """
    def __init__(self):
        self.cache = []

    def build(self, directory):
        # find all files in the transmitter directory with the name 
        # usbinfo.py
        paths = []
        n = 0
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                if (f == transmitter_file_name):
                    paths.append(os.path.abspath(os.path.join(dirpath, f)))

        for p in paths:
            module_name = "transmitter_file_" + str(n)
            n += 1
            loader = importlib.machinery.SourceFileLoader(module_name, p)
            transfile = loader.load_module()

            open_method = None
            read_channel_method = None
            close_method = None

            # some Matrix-level try-except embedding
            try:
                driver_package = None 
                try:
                    driver_package_path = (
                        transfile.driver_package_path
                    )
                    # then driver package given as file path
                    driver_loader = (
                        importlib.machinery.SourceFileLoader(
                            "driver_package_" + str(n),
                            driver_package_path
                        )
                    )
                    # may raise FileNotFoundError
                    driver_package = driver_loader.load_module()
                except AttributeError: 
                    # then driver package given as module somewhere in
                    # system $PATH
                    driver_package_name = transfile.driver_package_name
                    # may raise AttributeError..$
                    driver_package = __import__(driver_package_name)

                try:
                    # assigning these methods may raise AttributeError...
                    open_method = driver_package.open
                    read_channel_method = driver_package.read_channel
                    close_method = driver_package.close

                    self.cache.append(
                        _TransmitterIdent(
                            transfile.manufacturer, 
                            transfile.name,
                            transfile.idVendor,
                            transfile.idProduct,
                            transfile.channel_units,
                            open_method,
                            read_channel_method,
                            close_method
                        )
                    )
                except AttributeError: 
                    # indicate malformed driver pkg
                    raise ImportError

            except AttributeError as e:
                # file was malformed
                pass

            except (ImportError, FileNotFoundError) as e:
                # driver package was malformed
                pass

    def find_by_vid_pid(self, vid, pid):
        for i in self.cache:
            if i.matches(vid, pid): return i

t_cache = _TransmitterCache()
t_cache.build(directory)

class TransmitterIndex:
    def filter(usb_list, cache=None):
        if cache is None: cache = t_cache # allows for testing
        transmitter_list = []
        for device in usb_list:
            transmitter = cache.find_by_vid_pid(
                device.idVendor,
                device.idProduct
            )
            if transmitter is not None:
                # combine transmitter data with bus number and address
                # and append to transmitter_list
                transmitter_list.append(
                    Transmitter(
                        bus=device.bus,
                        address=device.address,
                        manufacturer=transmitter.manufacturer,
                        name=transmitter.name,
                        vendor_id=device.idVendor,
                        product_id=device.idProduct,
                        num_channels=len(transmitter.channel_units),
                        channel_units=transmitter.channel_units,
                        open_method=transmitter.open_method,
                        read_channel_method=transmitter.read_channel_method,
                        close_method=transmitter.close_method
                    )
                )
        return transmitter_list
