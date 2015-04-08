import sys
from infrastructure.comm_bus import CommBus

class TransmitterController:
    def __init__(self, transmitter):
        self.transmitter = transmitter

    def stop(self, _signo, _stack_frame):
        self.transmitter.close()
        sys.exit(0)

    def run(self):
        for channel in self.transmitter.channels:
            updated = channel.update()
            if updated:
                CommBus.publish(channel.to_json())
