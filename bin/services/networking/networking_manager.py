import zmq
KILL_BROADCAST_FILTER = 10001
KILL_BROADCAST_ADDRESS = "tcp://127.0.0.1:5520"

USB_PAIR_ADDRESS = "ipc:///tmp/usbfeed"

TAC_ADDRESS = "tcp://127.0.0.1:6530"

EAC_PARENT_CHILD_BASE_PORT = 7590
EAC_PARENT_CHILD_N_ADDRESS = "tcp://127.0.0.1:{}"

class NetworkingManager:
    """
    Manager for this application that contains implementation of
    the messaging protocol used in this application and
    addressing information for each component. Addresses are
    not exposed externally
    This will most likely use ZeroMQ but if another method of
    communication is chosen you'll have to adhere to ZMQ
    terminology
    """
    POLLIN = zmq.POLLIN
    POLLOUT = zmq.POLLOUT

    @classmethod
    def KillBroadcastSubscriber(cls):
        return Subscriber(
            KILL_BROADCAST_ADDRESS,
            KILL_BROADCAST_FILTER
        )

    @classmethod
    def KillBroadcastPublisher(cls):
        return Publisher(
            KILL_BROADCAST_ADDRESS,
            KILL_BROADCAST_FILTER
        )


    @classmethod
    def UsbMonitorPairServer(cls):
        return PairServer(
            USB_PAIR_ADDRESS
        )

    @classmethod
    def UsbMonitorPairClient(cls):
        return PairClient(
            USB_PAIR_ADDRESS
        )

    @classmethod
    def TACParent(cls):
        return Router(
            TAC_ADDRESS
        )

    @classmethod
    def TACChild(cls, identity):
        ident = u'tac-child-%d' % int(identity)
        return Dealer(
            TAC_ADDRESS,
            ident
        )

    @classmethod
    def EACParentChildPairParentN(cls, n):
        return PairServer(
            EAC_PARENT_CHILD_N_ADDRESS.format(
                EAC_PARENT_CHILD_BASE_PORT+n
            )
        )

    @classmethod
    def EACParentChildPairChildN(cls, n):
        return PairClient(
            EAC_PARENT_CHILD_N_ADDRESS.format(
                EAC_PARENT_CHILD_BASE_PORT+n
            )
        )

    @classmethod
    def Poller(cls):
        return Poller()

class ZmqSocket:
    def contained_in(self, dct):
        # created because there was no way to maintain the ZMQ
        # syntax 'zmq.Socket() in dict(zmq.Poller().poll)'
        # without some clunky inheritance/exposure of wrapped socket
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

        self.address = address
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

    def unbind(self):
        self.wrapped.unbind(self.address)

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

class Router(ZmqSocket):
    def __init__(self, address):
        context = zmq.Context()

        self.wrapped = context.socket(zmq.ROUTER)
        self.wrapped.bind(address)

    def send_multipart(self, args):
        self.wrapped.send_multipart(args)

    def recv_multipart(self):
        return self.wrapped.recv_multipart()

    def send_string(self, recipient_id, string):
        self.send_multipart(
            [recipient_id, string.encode('ascii')]
        )

    def recv_string(self):
        identity, string = self.recv_multipart()
        return [int(id), str(string)]

class Dealer(ZmqSocket):
    def __init__(self, address, identity):
        context = zmq.Context()

        self.identity = identity.encode('ascii')

        self.wrapped = context.socket(zmq.DEALER)
        self.wrapped.identity = self.identity
        self.wrapped.connect(address)

    def send_string(self, string):
        self.wrapped.send_string(string)

    def recv_string(self):
        return self.wrapped.recv_string()

    def recv(self):
        return self.wrapped.recv()

class Poller:
    def __init__(self):
        self.wrapped = zmq.Poller()

    def __contains__(self, wrapped_socket):
        return wrapped_socket in self.wrapped

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
