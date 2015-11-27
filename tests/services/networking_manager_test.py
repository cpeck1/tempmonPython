import unittest, time
from unittest.mock import MagicMock, patch

from bin.services.networking.networking_manager import NetworkingManager

class NetworkingManagerTest(unittest.TestCase):
    def setUp(self):
        self.poller = NetworkingManager.Poller()
    def tearDown(self):
        self.poller = None

class NetworkingManagerTestSuite(NetworkingManagerTest):
    def test_poller_pub_sub(self):
        """Poller registers Publish/Subscribe messages"""
        publisher = NetworkingManager.KillBroadcastPublisher()
        subscriber = NetworkingManager.KillBroadcastSubscriber()

        self.poller.register(subscriber, NetworkingManager.POLLIN)

        for _ in range(10):
            publisher.send_string("test_poller_pub_sub")
            time.sleep(0.001)

        socks = dict(self.poller.poll(200))
        self.assertTrue(subscriber.contained_in(socks))

    def test_poller_usb_pair_parent_send(self):
        """Poller registers Exclusive Pair (USB) messages from parent"""
        pair_parent = NetworkingManager.UsbMonitorPairServer()
        pair_child = NetworkingManager.UsbMonitorPairClient()

        self.poller.register(pair_child, NetworkingManager.POLLIN)

        for _ in range(10):
            pair_parent.send_string("test_poller_usb_pair_parent_send")
            time.sleep(0.001)

        socks = dict(self.poller.poll(200))
        self.assertTrue(pair_child.contained_in(socks))

    def test_poller_usb_pair_child_send(self):
        """Poller registers Exclusive Pair (USB) messages from child"""
        pair_parent = NetworkingManager.UsbMonitorPairServer()
        pair_child = NetworkingManager.UsbMonitorPairClient()

        self.poller.register(pair_parent, NetworkingManager.POLLIN)

        for _ in range(10):
            pair_child.send_string("test_poller_usb_pair_child_send")
            time.sleep(0.001)

        socks = dict(self.poller.poll(200))
        self.assertTrue(pair_parent.contained_in(socks))

    def test_kill_broadcast(self):
        """Subscriber receives messages properly from KillBroadcast publisher"""
        publisher = NetworkingManager.KillBroadcastPublisher()
        subscriber = NetworkingManager.KillBroadcastSubscriber()

        self.poller.register(subscriber, NetworkingManager.POLLIN)

        test_phrase = "TESTPHRASE"
        received_phrase = None
        tries = 0
        while not received_phrase and tries < 10:
            tries += 1
            publisher.send_string(test_phrase)
            time.sleep(0.001)
            socks = dict(self.poller.poll(10))
            if subscriber.contained_in(socks):
                received_msg = subscriber.recv_string()
                received_phrase = received_msg.split()[1]

        self.assertEqual(received_phrase, test_phrase)

    def test_usb_pair_two_way_communication(self):
        """Exclusive Pair (USB) two-way communication functions properly"""
        # let's play the telephone game!
        pair_parent = NetworkingManager.UsbMonitorPairServer()
        pair_child = NetworkingManager.UsbMonitorPairClient()

        self.poller.register(pair_parent, NetworkingManager.POLLIN)
        self.poller.register(pair_child, NetworkingManager.POLLIN)

        test_phrase = "test_usb_pair_two_way_communication"
        child_phrase = None
        parent_phrase = None

        for _ in range(10):
            pair_parent.send_string(test_phrase)
            time.sleep(0.001)
            socks = dict(self.poller.poll(10))
            if pair_child.contained_in(socks):
                child_phrase = pair_child.recv_string()
                break

        if child_phrase is not None:
            for _ in range(10):
                pair_child.send_string(child_phrase)
                time.sleep(0.001)
                socks = dict(self.poller.poll(10))
                if pair_parent.contained_in(socks):
                    parent_phrase = pair_parent.recv_string()
                    break

        self.assertEqual(parent_phrase, test_phrase)

    def test_eac_parent_child_fan_out_fan_in0(self):
        """Exclusive Pair (EAC) two-way communication functional (small scale)"""
        # ensure all children messaged report back, one child
        num_children = 1
        reported = 0
        parents = []
        unreported_children = []

        test_phrase = "test_eac_parent_child_fan_out"
        for i in range(num_children):
            parent = NetworkingManager.EACParentChildPairParentN(i)
            child = NetworkingManager.EACParentChildPairChildN(i)

            self.poller.register(parent, NetworkingManager.POLLIN)
            self.poller.register(child, NetworkingManager.POLLIN)

            parents.append(parent)
            unreported_children.append(child)

        for parent in parents:
            for _ in range(10):
                parent.send_string(test_phrase)
                time.sleep(0.001)

        self.poller.poll(200)
        for child in unreported_children:
            if child.contained_in(self.poller):
                string = child.recv_string()
                for _ in range(10):
                    child.send_string(string)

        self.poller.poll(200)
        for parent in parents:
            if parent.contained_in(self.poller):
                string = parent.recv_string()
                if string == test_phrase:
                    reported += 1

        self.assertEqual(reported, num_children)

    def test_eac_parent_child_fan_out_fan_in1(self):
        """Exclusive Pair (EAC) two-way communication functional (medium scale)"""
        # ensure all children messaged report back, few children
        num_children = 10
        reported = 0
        parents = []
        unreported_children = []

        test_phrase = "test_eac_parent_child_fan_out"
        for i in range(num_children):
            parent = NetworkingManager.EACParentChildPairParentN(i)
            child = NetworkingManager.EACParentChildPairChildN(i)

            self.poller.register(parent, NetworkingManager.POLLIN)
            self.poller.register(child, NetworkingManager.POLLIN)

            parents.append(parent)
            unreported_children.append(child)

        for parent in parents:
            for _ in range(10):
                parent.send_string(test_phrase)
                time.sleep(0.001)

        self.poller.poll(200)
        for child in unreported_children:
            if child.contained_in(self.poller):
                string = child.recv_string()
                for _ in range(10):
                    child.send_string(string)

        self.poller.poll(200)
        for parent in parents:
            if parent.contained_in(self.poller):
                string = parent.recv_string()
                if string == test_phrase:
                    reported += 1

        self.assertEqual(reported, num_children)

    def test_eac_parent_child_fan_out_fan_in2(self):
        """Exclusive Pair (EAC) two-way communication functional (large scale)"""
        # ensure all children messaged report back, many children
        num_children = 20
        reported = 0
        parents = []
        unreported_children = []

        test_phrase = "test_eac_parent_child_fan_out"
        for i in range(num_children):
            parent = NetworkingManager.EACParentChildPairParentN(i)
            child = NetworkingManager.EACParentChildPairChildN(i)

            self.poller.register(parent, NetworkingManager.POLLIN)
            self.poller.register(child, NetworkingManager.POLLIN)

            parents.append(parent)
            unreported_children.append(child)

        for parent in parents:
            for _ in range(10):
                parent.send_string(test_phrase)
                time.sleep(0.001)

        self.poller.poll(200)
        for child in unreported_children:
            if child.contained_in(self.poller):
                string = child.recv_string()
                for _ in range(10):
                    child.send_string(string)

        self.poller.poll(200)
        for parent in parents:
            if parent.contained_in(self.poller):
                string = parent.recv_string()
                if string == test_phrase:
                    reported += 1

        self.assertEqual(reported, num_children)

    def test_tac_parent_child_fan_out_fan_in0(self):
        """Router-Dealer (TAC) two-way communication functional (small scale)"""
        # ensure all children messaged report back, one child
        num_children = 1
        reported = 0
        parents = []
        unreported_children = []

        test_phrase = "test_tac_parent_child_fan_out"
        parent = NetworkingManager.TACParent()
        self.poller.register(parent, NetworkingManager.POLLIN)

        for i in range(num_children):
            child = NetworkingManager.TACChild(i)
            self.poller.register(child, NetworkingManager.POLLIN)
            unreported_children.append(child)

        for child in unreported_children:
            parent.send_string(child.identity, test_phrase)
            socks = dict(self.poller.poll())
            if child.contained_in(socks):
                string = child.recv_string()
                self.assertTrue(False)
                return
                for _ in range(10):
                    child.send_string(string)

        self.poller.poll(200)
        if parent.contained_in(self.poller):
            identity, string = parent.recv_string()
            if string == test_phrase:
                reported += 1

        self.assertEqual(reported, num_children)

    # def test_tac_parent_child_fan_out_fan_in1(self):
    #     """Exclusive Pair (TAC) two-way communication functional (medium scale)"""
    #     # ensure all children messaged report back, few children
    #     num_children = 10
    #     reported = 0
    #     parents = []
    #     unreported_children = []

    #     test_phrase = "test_tac_parent_child_fan_out"
    #     for i in range(num_children):
    #         parent = NetworkingManager.TACParentChildPairParentN(i)
    #         child = NetworkingManager.TACParentChildPairChildN(i)

    #         self.poller.register(parent, NetworkingManager.POLLIN)
    #         self.poller.register(child, NetworkingManager.POLLIN)

    #         parents.append(parent)
    #         unreported_children.append(child)

    #     for parent in parents:
    #         for _ in range(10):
    #             parent.send_string(test_phrase)
    #             time.sleep(0.001)

    #     self.poller.poll(200)
    #     for child in unreported_children:
    #         if child.contained_in(self.poller):
    #             string = child.recv_string()
    #             for _ in range(10):
    #                 child.send_string(string)

    #     self.poller.poll(200)
    #     for parent in parents:
    #         if parent.contained_in(self.poller):
    #             string = parent.recv_string()
    #             if string == test_phrase:
    #                 reported += 1

    #     self.assertEqual(reported, num_children)

    # def test_tac_parent_child_fan_out_fan_in2(self):
    #     """Exclusive Pair (TAC) two-way communication functional (large scale)"""
    #     # ensure all children messaged report back, many children
    #     num_children = 20
    #     reported = 0
    #     parents = []
    #     unreported_children = []

    #     test_phrase = "test_tac_parent_child_fan_out"
    #     for i in range(num_children):
    #         parent = NetworkingManager.TACParentChildPairParentN(i)
    #         child = NetworkingManager.TACParentChildPairChildN(i)

    #         self.poller.register(parent, NetworkingManager.POLLIN)
    #         self.poller.register(child, NetworkingManager.POLLIN)

    #         parents.append(parent)
    #         unreported_children.append(child)

    #     for parent in parents:
    #         for _ in range(10):
    #             parent.send_string(test_phrase)
    #             time.sleep(0.001)

    #     self.poller.poll(200)
    #     for child in unreported_children:
    #         if child.contained_in(self.poller):
    #             string = child.recv_string()
    #             for _ in range(10):
    #                 child.send_string(string)

    #     self.poller.poll(200)
    #     for parent in parents:
    #         if parent.contained_in(self.poller):
    #             string = parent.recv_string()
    #             if string == test_phrase:
    #                 reported += 1

    #     self.assertEqual(reported, num_children)

