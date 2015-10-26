import signal, logging, random, time
import json

from multiprocessing import Process

from bin.infrastructure.comm_bus import CommBus

logger = logging.getLogger("monitoring_application")

class TransmitterController:
    def __init__(self, transmitter):
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)

        self.transmitter = transmitter

        self.transmitter.open()
        logger.info(
            "Transmitter controller application started using " +
            repr(transmitter)
        )

    def stop(self, _signo, _stack_frame):
        self.transmitter.close()
        logger.info(
            "Transmitter controller application stopped using " +
            repr(self.transmitter)
        )
        exit(0)

    def run(self):
        while True:
            time.sleep(1)
            for channel in self.transmitter.channels:
                updated = channel.update()
                if updated:
                    logger.info(
                        json.dumps(
                            channel,
                            default=lambda o: o.__dict__
                        )
                    )

