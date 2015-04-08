import signal
import libusb1, usb1, usb.core, pyudev

from bin.services.transmitter_index import TransmitterIndex
from bin.infrastructure.usb_bus import *

class UsbPortController:
    def __init__(self):
        self.transmitter_applications = []
        signal.signal(signal.SIGTERM, self.stop)

        self.usb_bus = UsbBus.Instance()
        for device in usb.core.find(find_all=True):
            self.usb_bus.add(UsbDevice(device))

    def stop(self, _signo, _stack_frame):
        for app in transmitter_applications:
            app.stop(_signo, _stack_frame)

        logger.info("USB Port Controller stopping")
        sys.exit(0)

    def run(self): 
        # initially filter through the usb devices already present
        # in the system
        transmitters = TransmitterIndex.filter(self.usb_bus)
        for transmitter in transmitters:
            tc = TransmitterController(transmitter)

            transmitter_application = Process(target=tc.run)
            transmitter_application.start()

            self.transmitter_applications.append(transmitter_application)
        # watch for connecting and disconnecting usb devices; if a 
        # transmitter is disconnected, signal for the corresponding
        # transmitter_application to stop; if a transmitter is connected
        # create a new transmitter_application with the new transmitter
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb', device_type='usb_device')
        monitor.start()
        for device in iter(monitor.poll, None):
            # if the device is being removed, find it within the bus
            # we can tell a device is being removed if it has no 
            # attributes
            if not device.attributes:
                usb_device = self.usb_bus.find_with(path=device.path)
                for app in self.transmitter_applications:
                    if app.transmitter.usb_device == usb_device:
                        app.stop(None, None) 
            else:
                usb_device = UsbDevice(device)
                self.usb_bus.add(usb_device)
                
                transmitter = TransmitterIndex.find_matching(usb_device)
                if transmitter is not None:
                    tc = TransmitterController(transmitter)
                    transmitter_application = Process(target=tc.run)
                    transmitter_application.start()
                    self.transmitter_applications.append(
                        transmitter_application
                    )
