import unittest

from bin.models.request_buffer import RequestBuffer

class FakeRequest:
    def __init__(self, id, expired):
        self.id = id
        self._expired = expired
        self.dispatched = False

    def expired(self):
        return self._expired

    def correlates_with(self, reply):
        return self.id == reply.id

    def dispatch(self):
        self.dispatched = True

class FakeReply:
    def __init__(self, id):
        self.id = id

class RequestBufferTest(unittest.TestCase):
    def setUp(self):
        self.request_buffer = RequestBuffer()
    def tearDown(self):
        self.request_buffer = None

class RequestBufferTestSuite(RequestBufferTest):
    def test_append(self):
        """RequestBuffer append should add to the buffer's request list"""
        req = FakeRequest(12345, True)

        self.request_buffer.append(req)
        appended_req = self.request_buffer.requests[0]

        self.assertEqual(appended_req, req)

    def test_remove_expired(self):
        """RequestBuffer remove_expired removes all requests that are expired"""
        req1 = FakeRequest(1, True)
        req2 = FakeRequest(2, False)
        req3 = FakeRequest(3, True)
        req4 = FakeRequest(4, True)
        req5 = FakeRequest(5, False)
        self.request_buffer.append(req1)
        self.request_buffer.append(req2)
        self.request_buffer.append(req3)
        self.request_buffer.append(req4)
        self.request_buffer.append(req5)

        self.request_buffer.remove_expired()

        self.assertTrue(
            req2 in self.request_buffer.requests and
            req5 in self.request_buffer.requests
        )

    def test_dispatch_all0(self):
        """RequestBuffer dispatch_all dispatches all requests in request buffer"""
        req1 = FakeRequest(1, False)
        req2 = FakeRequest(2, False)
        req3 = FakeRequest(3, False)
        req4 = FakeRequest(4, False)
        req5 = FakeRequest(5, False)

        self.request_buffer.append(req1)
        self.request_buffer.append(req2)
        self.request_buffer.append(req3)
        self.request_buffer.append(req4)
        self.request_buffer.append(req5)

        self.request_buffer.dispatch_all()

        self.assertEqual(
            [True]*5,
            [req.dispatched for req in self.request_buffer.requests]
        )

    def test_dispatch_all1(self):
        """RequestBuffer dispatch_all removes expired requests when dispatching"""
        req1 = FakeRequest(1, True) # expired
        req2 = FakeRequest(2, False) # not expired
        req3 = FakeRequest(3, True)
        req4 = FakeRequest(4, False)
        req5 = FakeRequest(5, False)

        self.request_buffer.append(req1)
        self.request_buffer.append(req2)
        self.request_buffer.append(req3)
        self.request_buffer.append(req4)
        self.request_buffer.append(req5)

        self.request_buffer.dispatch_all()

        self.assertTrue(
            req1 not in self.request_buffer.requests and
            req2 in self.request_buffer.requests and
            req3 not in self.request_buffer.requests and
            req4 in self.request_buffer.requests and
            req5 in self.request_buffer.requests
        )

    def test_process_reply0(self):
        """RequestBuffer process_reply does nothing if no request correlates"""
        req1 = FakeRequest(1, True) # expired
        req2 = FakeRequest(2, False) # not expired
        req3 = FakeRequest(3, True)
        req4 = FakeRequest(4, False)
        req5 = FakeRequest(5, False)

        self.request_buffer.append(req1)
        self.request_buffer.append(req2)
        self.request_buffer.append(req3)
        self.request_buffer.append(req4)
        self.request_buffer.append(req5)

        reply = FakeReply(id=6)

        self.request_buffer.process_reply(reply)
        self.assertEqual(len(self.request_buffer.requests), 5)

    def test_process_reply0(self):
        """RequestBuffer process_reply does nothing if no request correlates"""
        req1 = FakeRequest(1, True) # expired
        req2 = FakeRequest(2, False) # not expired
        req3 = FakeRequest(3, True)
        req4 = FakeRequest(4, False)
        req5 = FakeRequest(5, False)

        self.request_buffer.append(req1)
        self.request_buffer.append(req2)
        self.request_buffer.append(req3)
        self.request_buffer.append(req4)
        self.request_buffer.append(req5)

        reply = FakeReply(id=5)

        self.request_buffer.process_reply(reply)

        self.assertTrue(
            req1 in self.request_buffer.requests and
            req2 in self.request_buffer.requests and
            req3 in self.request_buffer.requests and
            req4 in self.request_buffer.requests and
            req5 not in self.request_buffer.requests
        )
