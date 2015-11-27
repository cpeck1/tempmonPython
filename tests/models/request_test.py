import unittest

from bin.models.request import Request

class FakeReply:
    def __init__(self, id):
        self.id = id

class RequestTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

class RequestTestSuite(RequestTest):
    def test_request_dispatch0(self):
        """Request dispatch executes dispatcher normally and returns retval"""
        r = Request(id=1, dispatcher=lambda o: o, args=[1, 2, 3, 4])

        self.assertEqual(r.dispatch(), [1, 2, 3, 4])

    def test_request_dispatch1(self):
        """Request that raises an exception raises an exception"""
        r = Request(id=1, dispatcher=lambda o: None+o, args=1)

        with self.assertRaises(TypeError):
            r.dispatch()

    def test_request_dispatch2(self):
        """Request that specifies splat_args splats args in dispatch call"""
        r = Request(
            id=1,
            dispatcher=lambda x, y: x+y,
            args=[1, 2],
            splat_args=True
        )
        self.assertEqual(r.dispatch(), 3)

    def test_reaches_max_hops(self):
        """Request exipires by default after one dispatch"""
        r = Request(id=1, dispatcher=lambda o: o, args=1)
        r.dispatch()

        self.assertTrue(r.expired())

    def test_reaches_max_hops1(self):
        """Request expires with non-default value after appropriate amount of time"""
        r = Request(id=1, dispatcher=lambda o: o, args=1, hop_limit=5)

        for _ in range(5):
            r.dispatch()

        self.assertTrue(r.expired())

    def test_does_not_reach_max_hops0(self):
        """Request does not expire with default value after no dispatches"""
        r = Request(id=1, dispatcher=lambda o: o, args=1, hop_limit=5)

        self.assertFalse(r.expired())

    def test_does_not_reach_max_hops1(self):
        """Request does not expire with non-default value after a few dispatches"""
        r = Request(id=1, dispatcher=lambda o: o, args=1, hop_limit=5)

        for _ in range(3):
            r.dispatch()

        self.assertFalse(r.expired())

    def test_correlates_with0(self):
        """Request does not correlate with 'message' whose id does not match"""
        test_id = "1234567835415432534"
        request = Request(id=test_id, dispatcher=lambda o: o, args=1)

        fake_reply = FakeReply(id=test_id[0:-1])

        self.assertFalse(request.correlates_with(fake_reply))

    def test_correlates_with1(self):
        """Request does correlate with 'message' whose id matches"""
        test_id = "1234567835415432534"
        request = Request(id=test_id, dispatcher=lambda o: o, args=1)

        fake_reply = FakeReply(id=test_id)

        self.assertTrue(request.correlates_with(fake_reply))


