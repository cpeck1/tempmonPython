# append the project bin to the sys search path
import unittest
from datetime import datetime
import time

from alarm import Alarm

class AlarmTest(unittest.TestCase):
    def setUp(self):
        self.alarm = Alarm(1342)

    def tearDown(self):
        self.alarm = None

class DefaultUninitializedStateTest(AlarmTest):
    def test_default_cause(self):
        self.assertEqual(
            self.alarm.cause, None,
            'incorrect default alarm cause')
    
    def test_default_start_time(self):
        self.assertEqual(
            self.alarm.start_time, None, 
            'incorrect default alarm start time')

    def test_default_refresh_time(self):
        self.assertEqual(
            self.alarm.last_refresh_time, None, 
            'incorrect default alarm last refresh time')

    def test_default_end_time(self):
        self.assertEqual(
            self.alarm.end_time, None, 
            'incorrect default alarm end time')

class AccessorTest(AlarmTest):
    def test_container_id(self):
        container_id = 1342
        self.assertEqual(
            self.alarm.container_id, container_id,
            'incorrect container id retrieved')

    def test_get_set_category1(self):
        set_str = ""
        self.alarm.category = set_str
        get_str = self.alarm.category
        self.assertEqual(
            set_str, get_str,
            "incorrect category set or retrieved")

    def test_get_set_category2(self):
        set_str = "Unit test 1"
        self.alarm.category = set_str
        get_str = self.alarm.category
        self.assertEqual(
            set_str, get_str, 
            "incorrect category set or retrieved")
    def test_get_set_start_time1(self):
        set_time = datetime(1970, 9, 10, 12, 30)
        self.alarm.start_time = set_time
        get_time = self.alarm.start_time
        self.assertEqual(
            set_time, get_time,
            "incorrect start time set or retrieved")

    def test_get_set_start_time2(self):
        set_time = datetime(1980, 1, 12, 23, 41, 49)
        self.alarm.start_time = set_time
        get_time = self.alarm.start_time
        self.assertEqual(
            set_time, get_time,
            "incorrect start time set or retrieved")

    def test_get_set_start_time3(self):
        set_time = datetime(1990, 12, 1, 0, 0, 12, 90)
        self.alarm.start_time = set_time
        get_time = self.alarm.start_time
        self.assertEqual(
            set_time, get_time,
            "incorrect start time set or retrieved")

    def set_start_time(self, time):
        self.alarm.start_time = time

    def test_set_start_time_bad_type1(self):
        set_time = None
        self.assertRaises(
            AssertionError, self.set_start_time, set_time)
            
    def test_set_start_time_bad_type2(self):
        set_time = time.localtime
        self.assertRaises(
            AssertionError, self.set_start_time, set_time)

    def test_set_start_time_bad_type3(self):
        set_time = "2014-08-07 12:30:20"
        self.assertRaises(
            AssertionError, self.set_start_time, set_time)

    def test_get_set_refresh_time1(self):
        set_time = datetime(1970, 9, 10, 12, 30)
        self.alarm.last_refresh_time = set_time
        get_time = self.alarm.last_refresh_time
        self.assertEqual(
            set_time, get_time,
            "incorrect start time set or retrieved")

    def test_get_set_refresh_time2(self):
        set_time = datetime(1970, 9, 10, 12, 30, 23)
        self.alarm.last_refresh_time = set_time
        get_time = self.alarm.last_refresh_time
        self.assertEqual(
            set_time, get_time,
            "incorrect start time set or retrieved")
        
    def test_get_set_refresh_time3(self):
        set_time = datetime(1970, 9, 10, 12, 30, 23, 54)
        self.alarm.last_refresh_time = set_time
        get_time = self.alarm.last_refresh_time
        self.assertEqual(
            set_time, get_time,
            "incorrect start time set or retrieved")

    def set_last_refresh_time(self, time):
        self.alarm.last_refresh_time = time

    def test_set_refresh_time_bad_type1(self):
        set_time = None
        self.assertRaises(
            AssertionError, self.set_last_refresh_time, set_time)

    def test_set_refresh_time_bad_type2(self):
        set_time = time.localtime
        self.assertRaises(
            AssertionError, self.set_last_refresh_time, set_time)

    def test_set_refresh_time_bad_type3(self):
        set_time = "2014-09-12 12:30:04"
        self.assertRaises(
            AssertionError, self.set_last_refresh_time, set_time)
        
    def test_get_set_end_time1(self):
        set_time = datetime(1970, 9, 10, 12, 30)
        self.alarm.end_time = set_time
        get_time = self.alarm.end_time
        self.assertEqual(
            set_time, get_time,
            "incorrect start time set or retrieved")
        
    def test_get_set_end_time2(self):
        set_time = datetime(1970, 9, 10, 12, 30, 23)
        self.alarm.end_time = set_time
        get_time = self.alarm.end_time
        self.assertEqual(
            set_time, get_time,
            "incorrect start time set or retrieved")

    def test_get_set_end_time3(self):
        set_time = datetime(1970, 9, 10, 12, 30, 23, 41)
        self.alarm.end_time = set_time
        get_time = self.alarm.end_time
        self.assertEqual(
            set_time, get_time,
            "incorrect start time set or retrieved")

    def set_end_time(self, time):
        self.alarm.end_time = time

    def test_set_end_time_type_error1(self):
        set_time = None
        self.assertRaises(
            AssertionError, self.set_end_time, set_time)

    def test_set_end_time_type_error2(self):
        set_time = time.localtime()
        self.assertRaises(
            AssertionError, self.set_end_time, set_time)

    def test_set_end_time_type_error3(self):
        set_time = "2014-08-07 12:23:03"
        self.assertRaises(
            AssertionError, self.set_end_time, set_time)

class ActivateTest(AlarmTest):
    def test_activate1(self):
        self.assertRaises(
            TypeError, self.alarm.activate)        

    def test_activate2(self):
        self.alarm.activate("test activate 2")
        self.assertTrue(
            isinstance(self.alarm.start_time, datetime),
            "did not set start time to correct type")

    def test_activate3(self):
        self.alarm.activate("test activate 3")
        start_time = self.alarm.start_time
        refresh_time = self.alarm.last_refresh_time
        self.assertEqual(
            start_time, refresh_time,
            "should set refresh time to start time")

    def test_activate4(self):
        self.alarm.activate("test activate 4")
        self.assertRaises(
            AssertionError, self.alarm.activate, "test activate 3")

class RefreshTest(AlarmTest):
    def test_refresh1(self):
        self.assertRaises(
            AssertionError, self.alarm.refresh)

    def test_refresh2(self):
        self.alarm.activate("test refresh 2")
        old_refresh_time = self.alarm.last_refresh_time
        self.alarm.refresh()
        new_refresh_time = self.alarm.last_refresh_time
        self.assertTrue(
            (isinstance(old_refresh_time, datetime)) and
            (isinstance(new_refresh_time, datetime)) and
            (old_refresh_time < new_refresh_time),
            "should increase last refresh time")

    def test_refresh3(self):
        self.alarm.activate("test refresh 3")
        self.alarm.end()

        self.assertRaises(
            AssertionError, self.alarm.refresh)

class EndTest(AlarmTest):
    def test_end1(self):
        self.assertRaises(
            AssertionError, self.alarm.end)

    def test_end2(self):
        self.alarm.activate("test end 2")
        self.alarm.end()
        
        st = self.alarm.start_time
        et = self.alarm.end_time
        now = datetime.now()
        self.assertTrue(
            (isinstance(st, datetime)) and
            (isinstance(et, datetime)) and
            (st < et < now),
            "should have an end time after start time and before now")

    def test_end3(self):
        self.alarm.activate("test end 3")
        self.alarm.end()

        self.assertRaises(
            AssertionError, self.alarm.end)

class IsGoingOffTest(AlarmTest):
    def is_going_off_test1(self):
        self.assertFalse(
            self.alarm.is_going_off(),
            "should not be going off after initialization")
        
    def is_going_off_test2(self):
        self.alarm.activate("is going off test 2")
        self.assertTrue(
            self.alarm.is_going_off(),
            "should be going off after activation")

    def is_going_off_test3(self):
        self.alarm.activate("is going off test 3")
        self.alarm.end()
        self.assertFalse(
            self.alarm.is_going_off(),
            "should not be going off after ending")
            
class HasEndedTest(AlarmTest):
    def has_ended_test1(self):
        self.assertFalse(
            self.alarm.has_ended(),
            "should not have ended before activation")

    def has_ended_test2(self):
        self.alarm.activate("has ended test 2")
        self.assertFalse(
            self.alarm.has_ended(),
            "should not have ended after activation and before ending")
        
    def has_ended_test3(self):
        self.alarm.activate("has ended test 3")
        self.alarm.end()
        self.assertTrue(
            self.alarm.has_ended(),
            "should have ended after activating and ending (dat logic)")

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test)
    unittest.TextTestRunner().run(suite)
