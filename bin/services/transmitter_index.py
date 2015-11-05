import os, sys, logging
import importlib.machinery
from bin.models.transmitter import Transmitter

logger = logging.getLogger("monitoring_application")

directory = "/home/connor/workspace/tempmonPython/bin/transmitters"
transmitter_file_name = "usbinfo.py"
# sort of a case class, shell for holding a few pieces of data
class _TransmitterIdent:
    def __init__(
            self,
            idVendor,
            idProduct,
            manufacturer,
            product,
            channel_units,
            open_method,
            read_channel_method,
            close_method
    ):
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.manufacturer = manufacturer
        self.product = product
        self.channel_units = channel_units

        self.open_method = open_method
        self.read_channel_method = read_channel_method
        self.close_method = close_method

    def __repr__(self):
        return "_TransmitterIdent({}, {}, {}, {})".format(
            self.channel_units,
            self.open_method,
            self.read_channel_method,
            self.close_method
        )

    def matches(self, vid, pid):
        return ((self.idVendor == vid) and (self.idProduct == pid))

class _TransmitterCache:
    """
    cache of transmitters from the transmitter package based on
    the transmitter_file_name modules inside, which contain the
    manufacturer, product, product and vendor ids of each transmitter
    within the system
    """
    def __init__(self):
        self.cache = []

    def get_paths_to(self, directory, filename):
        paths = []
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                if (f == filename):
                    paths.append(os.path.abspath(os.path.join(dirpath, f)))
        return paths

    def load_driver_package(self, module, n):
        # module: the python package the driver package is coming from
        # n: identifier for driver package, helps reduce redundancies
        try:
            driver_package = None
            try:
                driver_package_path = (
                    module.driver_package_path
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
                return driver_package
            except AttributeError as e:
                # then driver package given as module somewhere in
                # system $PATH (maybe)
                driver_package_name = module.driver_package_name
                # may raise AttributeError..$
                driver_package = __import__(driver_package_name)
                return driver_package
        except (AttributeError, FileNotFoundError) as e:
            logger.error("Failed to import driver package: " + str(e))
            return None

    def build(self, directory):
        # find all files in the transmitter directory with the name
        # usbinfo.py
        paths = self.get_paths_to(directory, transmitter_file_name)
        n = 0
        for p in paths:
            module_name = "transmitter_file_" + str(n)
            # this is mostly for testing purposes
            if module_name in sys.modules:
                del sys.modules[module_name]

            n += 1
            loader = importlib.machinery.SourceFileLoader(module_name, p)
            try:
                module = loader.load_module()
            except Exception as e:
                # exceptions will only occur if there are exceptions in
                # the usbinfo.py file; literally any exception may occur
                # in the file so don't try to predict end user stupidity
                logger.error(
                    "The transmitter file in the path "+p+" contained "+\
                    "the following error: " + str(e)
                )
                continue

            driver_package = self.load_driver_package(module, n)
            # assigning these methods may raise AttributeError
            try:
                self.cache.append(
                    _TransmitterIdent(
                        module.idVendor,
                        module.idProduct,
                        module.manufacturer,
                        module.product,
                        module.channel_units,
                        driver_package.open_method,
                        driver_package.read_channel_method,
                        driver_package.close_method
                    )
                )
            except AttributeError as e:
                # driver package was malformed
                logger.error(
                    "The transmitter file in the path " + p +\
                    " contained the following error: " + str(e)
                )


    def find_by_vid_pid(self, vid, pid):
        for i in self.cache:
            if i.matches(vid, pid): return i

t_cache = _TransmitterCache()
t_cache.build(directory)

class TransmitterIndex:
    def find_matching(device, cache=None):
        for trans in t_cache.cache:
            logger.info(repr(trans))

        if cache is None: cache = t_cache # allows for testing
        transmitter = cache.find_by_vid_pid(
            device.idVendor,
            device.idProduct
        )
        if transmitter is not None:
            return Transmitter(
                usb_device=device,
                num_channels=len(transmitter.channel_units),
                channel_units=transmitter.channel_units,
                open_method=transmitter.open_method,
                read_channel_method=transmitter.read_channel_method,
                close_method=transmitter.close_method
            )

    def filter(usb_list, cache=None):
        for trans in t_cache.cache:
            logger.info(repr(trans))

        if cache is None: cache = t_cache # allows for testing
        transmitter_list = []
        for device in usb_list.devices:
            transmitter = cache.find_by_vid_pid(
                device.idVendor,
                device.idProduct
            )
            if transmitter is not None:
                # combine transmitter data with bus number and address
                # and append to transmitter_list
                transmitter_list.append(
                    Transmitter(
                        usb_device=device,
                        num_channels=len(transmitter.channel_units),
                        channel_units=transmitter.channel_units,
                        open_method=transmitter.open_method,
                        read_channel_method=transmitter.read_channel_method,
                        close_method=transmitter.close_method
                    )
                )
        return transmitter_list
