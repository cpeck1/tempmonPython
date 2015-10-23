import sys, signal, logging, random, time
import libusb1, usb1, usb.core, pyudev
import json

from multiprocessing import Process

from bin.services.transmitter_index import TransmitterIndex
from bin.infrastructure.usb_bus import *

logger = logging.getLogger("monitoring_application")

class Message():
    def __init__(self, action, usb_device):
        self.source = 'usb_port_controller'
        self.usb_device = usb_device
        self.action = action

    def jsonify(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class CommunicationsBus:
    def __init__(self):
        pass

    def listen(self):
        return Message()

    def send(self, destination, message):
        print(message.jsonify())


class UsbPortController:
    def __init__(self):
        signal.signal(signal.SIGTERM, self.stop)

        self.comm_bus = CommunicationsBus()
        self.observer = None

        self.usb_bus = UsbBus.Instance()

        # initially filter through the usb devices already present
        # in the system
        for usb_device in self.usb_bus.devices:
            message = Message('add', usb_device)
            self.comm_bus.send('transmitter_application_controller', message)

    def stop(self, _signo, _stack_frame):
        self.observer.stop()

        logger.info("USB Port Controller stopping")

    def handle_event(self, action, device):
        '''
        action: the action that caused this event (eg add, remove)
        device: the usb device that prompted the event
        '''
        if not device.attributes:
            usb_device = self.usb_bus.find_with(path=device.device_path)
        else:
            usb_device = UsbDevice(device)
            self.usb_bus.add(usb_device)

        message = Message(action, usb_device)
        self.comm_bus.send('transmitter_application_controller', message)

    def run(self):
        logger.info("Usb Port Controller starting")

        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb', device_type='usb_device')
        self.observer = pyudev.MonitorObserver(monitor, self.handle_event)
        self.observer.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.stop(None, None)

