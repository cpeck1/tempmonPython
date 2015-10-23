import signal, logging, random, time
import json

from multiprocessing import Process

from bin.services.usb_library_translator import PyusbDevice
from bin.infrastructure.usb_bus import UsbDevice
from bin.services.transmitter_index import TransmitterIndex
from bin.controllers.transmitter_controller import TransmitterController

from bin.models.exceptions import DeviceNotFoundError

logger = logging.getLogger("monitoring_application")

class Message:
    def __init__(self, action):
        """
        what a message might look like (but hopefully less shitty)
        """
        self.source = 'usb_port_controller'
        self.action = action
        try:
            self.usb_device = json.dumps(
                UsbDevice.from_attributes(
                    idVendor=0x05ac,
                    idProduct=0x1261
                ),
                default=lambda o: o.__dict__
            )
        except DeviceNotFoundError:
            self.source = None
            self.action = None
            return

class CommunicationsBus:
    def __init__(self):
        pass

    def listen(self):
        print("message received")
        return Message(random.choice(['add', 'remove']))

    def send(self, message):
        print(message)

class __TransmitterApplication:
    """
    Class for holding a transmitter application and its python
    multiprocessing process. Less clunky than dealing with a tuple
    """
    def __init__(self, controller, process):
        self.controller = controller
        self.process = process

class TransmitterApplicationController:
    def __init__(self):
        signal.signal(signal.SIGTERM, self.stop)
        self.process = Process(target=self.run)

        self.comm_bus = CommunicationsBus()
        self.transmitter_applications = []

        logger.info("Transmitter Application Controller starting")

    def stop(self, _signo, _stack_frame):
        for app in self.transmitter_applications:
            pass

        logger.info("Transmitter Application Controller stopping")

    def start_transmitter_application_using(self, transmitter):
        for app in self.transmitter_applications:
            if app.controller.transmitter.usb_device == transmitter.usb_device:
                logger.info(
                    "Process using "+repr(transmitter)+" already running"
                )
                return

        controller = TransmitterController(transmitter)
        process = Process(target=controller.run)
        process.start()
        self.transmitter_applications.append(
            __TransmitterApplication(controller, process)
        )

    def stop_transmitter_application_using(self, transmitter):
        for app in self.transmitter_applications:
            if app.controller.transmitter.usb_device == transmitter.usb_device:
                app.process.terminate()
                self.transmitter_applications.remove(app)

    def run(self):
        while True:
            message = self.comm_bus.listen()
            if message.source == 'usb_port_controller':
                # usb_device = json.decode(message.usb_device)
                try:
                    usb_device = UsbDevice.from_json(message.usb_device)
                except:
                    print("No device found matching those attributes")

                transmitter = TransmitterIndex.find_matching(usb_device)
                if transmitter:
                    if message.action == 'add':
                        self.start_transmitter_application_using(transmitter)
                    elif message.action == 'remove':
                        self.stop_transmitter_application_using(transmitter)

            elif message.source == 'application_manager':
                usb_device = UsbDevice.from_json(message.usb_device)
                transmitter = TransmitterIndex.find_matching(usb_device)
                if transmitter:
                    if message.action == 'add':
                        self.start_transmitter_application_using(transmitter)
                    elif message.action == 'remove':
                        self.stop_transmitter_application_using(transmitter)
            time.sleep(5)
