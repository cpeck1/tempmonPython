import zmq

class NetworkingManager:
    """
    This will most likely use ZeroMQ but if another method of
    communication is chosen you'll have to adhere to ZMQ
    terminology
    """
    KILL_BROADCAST_FILTER = 10001
    KILL_BROADCAST_ADDRESS = "tcp://127.0.0.1:5520"

    USB_PAIR_ADDRESS = "tcp://127.0.0.1:5550"

    TAC_PARENT_CHILD_BASE_PORT = 5590
    TAC_PARENT_CHILD_N_ADDRESS = "tcp://127.0.0.1:{}"

    EAC_PARENT_CHILD_BASE_PORT = 7590
    EAC_PARENT_CHILD_N_ADDRESS = "tcp://127.0.0.1:{}"

    POLLIN = zmq.POLLIN
    POLLOUT = zmq.POLLOUT

    @classmethod
    def KillBroadcastSubscriber(cls):
        return Subscriber(
            cls.KILL_BROADCAST_ADDRESS,
            cls.KILL_BROADCAST_FILTER
        )

    @classmethod
    def KillBroadcastPublisher(cls):
        return Publisher(
            cls.KILL_BROADCAST_ADDRESS,
            cls.KILL_BROADCAST_FILTER
        )


    @classmethod
    def UsbMonitorPairServer(cls):
        return PairServer(
            cls.USB_PAIR_ADDRESS
        )

    @classmethod
    def UsbMonitorPairClient(cls):
        return PairClient(
            cls.USB_PAIR_ADDRESS
        )

    @classmethod
    def TACParentChildNPairParent(cls, n):
        return PairServer(
            cls.TAC_PARENT_CHILD_N_ADDRESS.format(
                cls.TAC_PARENT_CHILD_BASE_PORT+n
            )
        )

    @classmethod
    def TACParentChildNPairChild(cls, n):
        return PairClient(
            cls.TAC_PARENT_CHILD_N_ADDRESS.format(
                cls.TAC_PARENT_CHILD_BASE_PORT+n
            )
        )

    @classmethod
    def EACParentChildNPairParent(cls, n):
        return PairServer(
            cls.EAC_PARENT_CHILD_N_ADDRESS.format(
                cls.EAC_PARENT_CHILD_BASE_PORT+n
            )
        )

    @classmethod
    def EACParentChildNPairChild(cls, n):
        return PairClient(
            cls.EAC_PARENT_CHILD_N_ADDRESS.format(
                cls.EAC_PARENT_CHILD_BASE_PORT+n
            )
        )

    @classmethod
    def Poller(cls):
        return Poller()

class ZmqSocket:
    def contained_in(self, dct):
        return self.wrapped in dct

class Subscriber(ZmqSocket):
    def __init__(self, address, filter):
        context = zmq.Context()
        self.wrapped = context.socket(zmq.SUB)

        self.wrapped.connect(address)
        self.wrapped.setsockopt_string(
            zmq.SUBSCRIBE,
            str(filter)
        )

    def recv_string(self):
        return self.wrapped.recv_string()

class Publisher(ZmqSocket):
    def __init__(self, address, filter):
        context = zmq.Context()

        self.filter = filter
        self.wrapped = context.socket(zmq.PUB)
        self.wrapped.bind(address)

    def send_string(self, string):
        self.wrapped.send_string(
            "{} {}".format(
                self.filter,
                string
            )
        )

class Pair(ZmqSocket):
    def recv_string(self):
        return self.wrapped.recv_string()

    def send_string(self, string):
        self.wrapped.send_string(string)

class PairServer(Pair):
    def __init__(self, address):
        context = zmq.Context()

        self.address = address

        self.wrapped = context.socket(zmq.PAIR)
        self.wrapped.bind(address)

    def unbind(self):
        self.wrapped.unbind(self.address)

class PairClient(Pair):
    def __init__(self, address):
        context = zmq.Context()

        self.wrapped = context.socket(zmq.PAIR)
        self.wrapped.connect(address)

class Poller:
    def __init__(self):
        self.wrapped = zmq.Poller()

    def __contains__(self, wrapped_socket):
        return wrapped_socket.wrapped in self.wrapped

    def modify(self, wrapped_socket, flags=zmq.POLLIN|zmq.POLLOUT):
        self.wrapped.modify(wrapped_socket.wrapped, flags)

    def unregister(self, wrapped_socket):
        self.wrapped.unregister(wrapped_socket.wrapped)

    def register(self, wrapped_socket, flags=zmq.POLLIN|zmq.POLLOUT):
        """
        Feels shitty I know
        """
        self.wrapped.register(wrapped_socket.wrapped, flags)

    def poll(self, timeout=None):
        return self.wrapped.poll(timeout)
