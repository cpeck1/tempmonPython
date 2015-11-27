import signal, logging, random, time
import json

from multiprocessing import Process

from bin.infrastructure.usb_bus import UsbDevice
from bin.infrastructure.operation import Operation

from bin.services.usb_library_translator import PyusbDevice
from bin.services.networking.networking_manager import NetworkingManager
from bin.services.networking.message import (
    Message,
    CommandMessage,
    DocumentMessage
)
from bin.services.transmitter_index import TransmitterIndex
from bin.services.command_processor import CommandProcessor

from bin.models.exceptions import (DeviceNotFoundError, ExitProcess)
from bin.models.usb_operation import UsbOperation
from bin.models.request import Request
from bin.models.request_buffer import RequestBuffer
from bin.models.command import Command

from bin.controllers.transmitter_controller import TransmitterController

logger = logging.getLogger("monitoring_application")

x = 0
ids = set()
def NEXT_CHILD_ID():
    global x
    global ids

    if not ids or (max(ids) > len(ids)):
        x = 1

    while x in ids:
        x += 1

    ids.add(x)
    return x

def REMOVE_CHILD_ID(id):
    try:
        ids.remove(id)
    except ValueError:
        pass

class _TransmitterApplication:
    """
    Class for holding a transmitter application and its python
    multiprocessing process.
    """
    def __init__(self, controller, process):
        self.controller = controller
        self.process = process

        self.last_request = None

class TransmitterApplicationController:
    def __init__(self):
        self.router = None
        self.poller = None
        self.transmitter_applications = dict()

        self.request_buffer = RequestBuffer()

    def process_usb_operation(self, usb_operation):
        transmitter = TransmitterIndex.find_matching(usb_operation.usb_device)
        if transmitter:
            if usb_operation.operation is Operation.ADD:
                self.start_transmitter_application(transmitter)
            elif usb_operation.operation is Operation.REMOVE:
                self.stop_transmitter_application(transmitter)

    def start_transmitter_application(self, transmitter):
        for child_id, app in self.transmitter_applications.items():
            if app.transmitter == transmitter:
                logger.error(
                    "Process using "+repr(transmitter)+" already running"
                )
                return

        child_id = NEXT_CHILD_ID()

        controller = TransmitterController(transmitter, child_id)
        process = Process(target=controller.run)

        process.daemon = True
        process.start()

        app = _TransmitterApplication(controller, process)
        self.transmitter_applications[child_id] = app

    def stop_transmitter_application(self, transmitter):
        for child_id, app in self.transmitter_applications.items():
            if app.transmitter == transmitter:
                message = CommandMessage(command=Command.SHUTDOWN)
                request = Request(
                    id=message.id,
                    dispatcher=self.router.send_string,
                    args=[child_id, message.serialize],
                    hop_limit=-1,
                    splat_args=True
                )
                self.request_buffer.append(request)

    def stop_all_transmitter_applications(self):
        for child_id, app in self.transmitter_applications:
            message = CommandMessage(command=Command.SHUTDOWN)
            request = Request(
                id=message.id,
                dispatcher=self.router.send_string,
                args=[child_id, message.serialize],
                hop_limit=-1,
                splat_args=True
            )
            self.request_buffer.append(request)
            app.last_request = message

    def run(self):
        logger.info("Transmitter Application Controller starting")

        # Kill broadcast subscriber
        kbsubscriber = NetworkingManager.KillBroadcastSubscriber()
        usb_monitor_pair = NetworkingManager.UsbMonitorPairClient()
        self.router = NetworkingManager.TACParent()

        self.poller = NetworkingManager.Poller()
        self.poller.register(kbsubscriber, NetworkingManager.POLLIN)
        self.poller.register(usb_monitor_pair, NetworkingManager.POLLIN)
        self.poller.register(self.router, NetworkingManager.POLLIN)

        while True:
            self.request_buffer.dispatch_all()
            socks = dict(self.poller.poll(50))

            if self.router.contained_in(socks):
                child_id, string = self.router.recv_string()
                # do some stuff with reply
                app = self.transmitter_applications[child_id]
                if app.last_request == Command.SHUTDOWN:
                    reply = CommandMessage.deserialize(string)
                    self.request_buffer.process_reply(reply)

                    if app.process.is_alive():
                        app.process.terminate()
                    del self.transmitter_applications[child_id]

            if usb_monitor_pair.contained_in(socks):
                # a message from the usb port controller indicates
                # a usb device has been added or removed from the system
                request = DocumentMessage.deserialize(
                    usb_monitor_pair.recv_string()
                )
                logger.info("Request received: " + request.serialize())
                usb_operation = UsbOperation.from_json(request.contents)
                self.process_usb_operation(usb_operation)
                # send a void reply to confirm receipt
                reply = CommandMessage.VoidReply(request)
                usb_monitor_pair.send_string(reply.serialize())

            if kbsubscriber.contained_in(socks):
                message = CommandMessage.deserialize(
                    kbsubscriber.recv_string()
                )
                reply_structure = None
                try:
                    command = Command(message.command)
                    command_processor = CommandProcessor(self)
                    reply_structure = command_processor.process(command)
                except ExitProcess:
                    self.request_buffer.clear()
                    self.stop_all_transmitter_applications()
                    self.request_buffer.dispatch_all()
                    logger.info("Transmitter Application Controller stopping")
                    break
                finally:
                    if reply_structure:
                        pass
