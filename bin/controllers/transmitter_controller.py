import signal, logging, random, time
import json

from bin.infrastructure.networking_library import NetworkingManager
from multiprocessing import Process

logger = logging.getLogger("monitoring_application")

class TransmitterController:
    def __init__(self, transmitter, child_num):
        self.transmitter = transmitter
        self.transmitter.open()

        self.child_num = child_num

    def update_channels(self):
        for channel in self.transmitter.channels:
            updated = channel.update()
            if updated:
                logger.info("Channel updated: " + repr(channel))

    def run(self):
        logger.info(
            "Transmitter controller application started using " +
            repr(self.transmitter)
        )

        kbsubscriber = NetworkingManager.KillBroadcastSubscriber()
        pair = NetworkingManager.TACParentChildNPairChild(self.child_num)

        poller = NetworkingManager.Poller()
        poller.register(kbsubscriber, NetworkingManager.POLLIN)
        poller.register(pair, NetworkingManager.POLLIN)

        while True:
            self.update_channels()

            socks = dict(poller.poll(1000))

            if pair.contained_in(socks):
                # no way to put this in function as break call needs
                # to be within while loop
                message = pair.recv_string()
                if message == "SHUTDOWN":
                    logger.info(
                        "Transmitter application with "+
                        repr(self.transmitter)+" stopping."
                    )
                    pair.send_string("OFFLINE")
                    break

            if kbsubscriber.contained_in(socks):
                message = kbsubscriber.recv_string()
                filter, command = message.split()

                if command == "KILL":
                    logger.info(
                        "Transmitter application with "+
                        repr(self.transmitter)+" stopping."
                    )
                    break

