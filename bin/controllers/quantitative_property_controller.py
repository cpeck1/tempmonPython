import time, signal, sys

from bin.models.quantitative_property import QuantitativeProperty
from bin.infrastructure.networking_library import NetworkingManager

import logging
logger = logging.getLogger("monitoring_application")

class QuantitativePropertyController:
    def __init__(self, dbsession, quantitative_property):
        signal.signal(signal.SIGTERM, self.stop)

        self.running = True

        self.dbsession = dbsession
        self.quantitative_property = quantitative_property

    def stop(self, _signo, _stack_frame):
        self.dbsession.commit()

        logger.warning(
            "Quantitative Property Controller forced to stop with " +
            repr(self.quantitative_property)
        )

        sys.exit(0)

    def run(self):
        logger.info(
            "Quantitative Property Controller starting with " +
            repr(self.quantitative_property)
        )

        subscriber = NetworkingManager.KillBroadcastSubscriber()

        poller = NetworkingManager.Poller()
        poller.register(subscriber, NetworkingManager.POLLIN)

        while True:
            socks = dict(poller.poll())

            if subscriber.contained_in(socks):
                message = subscriber.recv_string()
                filter, command = message.split()

                if command == "KILL":
                    logger.info("Quantitative Property Controller stopping")
                    break
