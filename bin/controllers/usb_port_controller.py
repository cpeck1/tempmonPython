import sys, logging, random, time
import libusb1, usb1, usb.core, pyudev
import json

from multiprocessing import Process

from bin.models.usb_operation import UsbOperation
from bin.models.command import Command
from bin.models.exceptions import ExitProcess
from bin.models.request import Request
from bin.models.request_buffer import RequestBuffer

from bin.services.transmitter_index import TransmitterIndex
from bin.services.command_processor import CommandProcessor
from bin.services.networking.networking_manager import NetworkingManager
from bin.services.networking.message import (
    Message, DocumentMessage, CommandMessage
)

from bin.infrastructure.usb_bus import *
from bin.infrastructure.operation import Operation

logger = logging.getLogger("monitoring_application")

class UsbPortController:
    def __init__(self):
        self.usb_bus = UsbBus.Instance()

        self.request_buffer = RequestBuffer()

    def handle_event(self, action, device):
        '''
        action: the action that caused this event (eg add, remove)
        device: the usb device that prompted the event
        '''
        operation = Operation(action)

        if not device.attributes:
            usb_device = self.usb_bus.find_with(path=device.device_path)
            new_op = UsbOperation(operation=operation, usb_device=usb_device)
            message = DocumentMessage(document=new_op.to_json())

            request = Request(
                id=message.id,
                dispatcher=self.usb_monitor_pair.send_string,
                args=message.serialize(),
                hop_limit=10
            )
            self.request_buffer.append(request)
            self.usb_bus.remove(usb_device)
        else:
            usb_device = UsbDevice(device)
            self.usb_bus.add(usb_device)
            new_op = UsbOperation(operation=operation, usb_device=usb_device)
            message = DocumentMessage(document=new_op.to_json())

            request = Request(
                id=message.id,
                dispatcher=self.usb_monitor_pair.send_string,
                args=message.serialize(),
                hop_limit=10
            )
            self.request_buffer.append(message)

    def run(self):
        logger.info("USB Port Controller starting")

        context = pyudev.Context()

        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb', device_type='usb_device')

        observer = pyudev.MonitorObserver(monitor, self.handle_event)
        observer.start()

        kbsubscriber = NetworkingManager.KillBroadcastSubscriber()
        usb_monitor_pair = NetworkingManager.UsbMonitorPairServer()

        poller = NetworkingManager.Poller()
        poller.register(kbsubscriber, NetworkingManager.POLLIN)
        poller.register(usb_monitor_pair, NetworkingManager.POLLIN)

        for device in self.usb_bus.devices:
            new_op = UsbOperation(
                usb_device=device,
                operation=Operation('add')
            )
            message = DocumentMessage(document=new_op.to_json())
            request = Request(
                id=message.id,
                dispatcher=usb_monitor_pair.send_string,
                args=message.serialize(),
                hop_limit=10
            )
            self.request_buffer.append(request)

        while True:
            self.request_buffer.dispatch_all()
            socks = dict(poller.poll(50))

            if usb_monitor_pair.contained_in(socks):
                reply = CommandMessage.deserialize(
                    usb_monitor_pair.recv_string()
                )
                self.request_buffer.process_reply(reply)

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
                    observer.stop()
                    usb_monitor_pair.unbind()
                    logger.info("USB Port Controller stopping")
                    break
                finally:
                    # send message if applicable
                    if reply_structure:
                        pass
