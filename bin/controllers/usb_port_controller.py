import sys, signal, logging, random, time
import libusb1, usb1, usb.core, pyudev
import json

from multiprocessing import Process

from bin.models.usb_operation import UsbOperation

from bin.services.transmitter_index import TransmitterIndex
from bin.infrastructure.usb_bus import *
from bin.infrastructure.networking_library import NetworkingManager
logger = logging.getLogger("monitoring_application")

class UsbPortController:
    def __init__(self):
        self.observer = None
        self.usb_bus = UsbBus.Instance()

        self.operations_pending = []
        for device in self.usb_bus.devices:
            new_op = UsbOperation(device, 'add')
            self.operations_pending.append(new_op)

    def handle_event(self, action, device):
        '''
        action: the action that caused this event (eg add, remove)
        device: the usb device that prompted the event
        '''
        if not device.attributes:
            usb_device = self.usb_bus.find_with(path=device.device_path)
            new_op = UsbOperation(usb_device, 'remove')
            self.operations_pending.append(new_op)
            self.usb_bus.remove(usb_device)
        else:
            usb_device = UsbDevice(device)
            logger.info("New USB device: "+repr(usb_device))
            self.usb_bus.add(usb_device)
            new_op = UsbOperation(usb_device, 'add')
            self.operations_pending.append(new_op)

    def dispatch_operations(self, pair):
        if self.operations_pending:
            operation = self.operations_pending[0]
            pair.send_string(operation.to_json())

    def run(self):
        logger.info("USB Port Controller starting")

        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb', device_type='usb_device')
        self.observer = pyudev.MonitorObserver(monitor, self.handle_event)
        self.observer.start()

        # Kill broadcast subscriber
        kbsubscriber = NetworkingManager.KillBroadcastSubscriber()
        usb_monitor_pair = NetworkingManager.UsbMonitorPairServer()

        poller = NetworkingManager.Poller()
        poller.register(kbsubscriber, NetworkingManager.POLLIN)
        poller.register(usb_monitor_pair, NetworkingManager.POLLIN)

        while True:
            self.dispatch_operations(usb_monitor_pair)

            socks = dict(poller.poll(50))

            if usb_monitor_pair.contained_in(socks):
                #TODO: replace with function
                message = usb_monitor_pair.recv_string()
                operation = UsbOperation.from_json(message)
                try:
                    self.operations_pending.remove(operation)
                except ValueError:
                    logger.info(
                        "Operation not found in pending operations"+
                        message
                    )

            if kbsubscriber.contained_in(socks):
                message = kbsubscriber.recv_string()
                filter, command = message.split()

                if command == "KILL":
                    logger.info("USB Port Controller stopping")
                    break
