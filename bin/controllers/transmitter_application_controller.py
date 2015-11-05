import signal, logging, random, time
import json

from multiprocessing import Process

from bin.services.usb_library_translator import PyusbDevice
from bin.infrastructure.usb_bus import UsbDevice
from bin.infrastructure.networking_library import NetworkingManager
from bin.services.transmitter_index import TransmitterIndex
from bin.controllers.transmitter_controller import TransmitterController

from bin.models.exceptions import DeviceNotFoundError
from bin.models.usb_operation import UsbOperation

logger = logging.getLogger("monitoring_application")

class _TransmitterApplication:
    shutdown_threshold = 100
    valid_statuses = {"ONLINE", "SHUTDOWN", "OFFLINE"}
    """
    Class for holding a transmitter application and its python
    multiprocessing process.
    """
    def __init__(self, controller, process, pair):
        self.controller = controller
        self.process = process
        self.pair = pair
        self._status = "ONLINE"

        self.shutdown_count = 0

    def transmitter_matches(self, transmitter):
        return (
            self.controller.transmitter.usb_device == transmitter.usb_device
        )

    def kill(self):
        self.process.terminate()

    def signal_shutdown(self):
        self.status = "SHUTDOWN"

    def shutting_down(self):
        return self.status == "SHUTDOWN"

    def shutdown(self):
        self.pair.send_string("SHUTDOWN")
        self.shutdown_count += 1

        if self.shutdown_count > _TransmitterApplication.shutdown_threshold:
            self.kill()

    def offline(self):
        return self.status == "OFFLINE"

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status in _TransmitterApplication.valid_statuses:
            self._status = status
        else:
            logger.error("Attempted to set invalid status: "+status)

class TransmitterApplicationController:
    def __init__(self):
        signal.signal(signal.SIGTERM, self.stop)

        self.poller = None
        self.transmitter_applications = []

    def stop(self, _signo, _stack_frame):
        # for app in self.transmitter_applications:
        #     app.process.terminate()

        # logger.info("Transmitter Application Controller stopping")
        # print("Stop triggered the following exception:" + repr(e))
        exit(0)

    def process_usb_operation(self, usb_operation):
        logger.info(
            "Processing usb operation with USB device: "+
            repr(usb_operation.usb_device) +
            " and operation: " +
            repr(usb_operation.operation)
        )
        transmitter = TransmitterIndex.find_matching(usb_operation.usb_device)
        if transmitter:
            if usb_operation.operation == 'add':
                self.start_transmitter_application_using(transmitter)
            elif usb_operation.operation == 'remove':
                self.signal_app_shutdown_using(transmitter)
        else:
            logger.info(
                repr(usb_operation.usb_device)+
                " is not a recognized transmitter on this system."
            )

    def start_transmitter_application_using(self, transmitter):
        for app in self.transmitter_applications:
            if app.transmitter_matches(transmitter):
                logger.info(
                    "Process using "+repr(transmitter)+" already running"
                )
                return

        child_num = len(self.transmitter_applications)

        controller = TransmitterController(transmitter, child_num)
        process = Process(target=controller.run)
        # exclusive pair for two-way TCP communication
        pair = NetworkingManager.TACParentChildNPairParent(child_num)
        self.poller.register(pair, NetworkingManager.POLLIN)

        process.daemon = True
        process.start()
        self.transmitter_applications.append(
            _TransmitterApplication(controller, process, pair)
        )

    def signal_app_shutdown_using(self, transmitter):
        logger.info("Signalling app shutdown with "+repr(transmitter))
        for app in self.transmitter_applications:
            if app.transmitter_matches(transmitter):
                # send terminate signal
                app.signal_shutdown()
                return
        logger.error(
            "No application's transmitter matches "+repr(transmitter)
        )

    def terminate_subprocesses(self):
        for app in self.transmitter_applications:
            logger.info(
                "Waiting for app with "+
                repr(app.controller.transmitter)+
                " to terminate..."
            )
            app.signal_shutdown()
            app.process.join(0.25)

            if app.process.is_alive():
                logger.warning(
                    "App with "+
                    repr(app.controller.transmitter)+
                    " did not terminate safely. Forcing termination..."
                )
                app.kill()

    def process_app_shutdowns(self):
        for app in self.transmitter_applications:
            if app.shutting_down():
                logger.info("Signalling app shutdown")
                app.shutdown()

    def delete_offline_applications(self):
        # avoids removing from list while iterating over it:
        offline = [
            app for app in self.transmitter_applications if app.offline()
        ]
        for app in offline:
            app.pair.unbind()
            try:
                self.transmitter_applications.remove(app)
            except ValueError:
                logger.error("Dafuq?")

    def run(self):
        logger.info("Transmitter Application Controller starting")

        # Kill broadcast subscriber
        kbsubscriber = NetworkingManager.KillBroadcastSubscriber()
        usb_monitor_pair = NetworkingManager.UsbMonitorPairClient()

        self.poller = NetworkingManager.Poller()
        self.poller.register(kbsubscriber, NetworkingManager.POLLIN)
        self.poller.register(usb_monitor_pair, NetworkingManager.POLLIN)

        while True:
            self.delete_offline_applications()
            self.process_app_shutdowns()

            socks = dict(self.poller.poll(50))

            for app in self.transmitter_applications:
                if app.pair.contained_in(socks):
                    app_status = app.pair.recv_string()
                    app.status = app_status

            if usb_monitor_pair.contained_in(socks):
                message = usb_monitor_pair.recv_string()
                operation = UsbOperation.from_json(message)
                self.process_usb_operation(operation)
                # bounce the message back to confirm receipt
                usb_monitor_pair.send_string(message)

            if kbsubscriber.contained_in(socks):
                message = kbsubscriber.recv_string()
                filter, command = message.split()

                if command == "KILL":
                    self.terminate_subprocesses()
                    logger.info("Transmitter Application Controller stopping")
                    break
