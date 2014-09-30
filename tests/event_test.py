import unittest
from datetime import datetime
import time

from event import Event

class EventTest(unittest.TestCase):
    def setUp(self):
        self.event = Event(1342)

    def tearDown(self):
        self.event = None

class DefaultUninitializedStateTest(EventTest):
    def test_default_context_id(self):
        cid = self.event.context_id
        self.assertEqual(cid, 1342)

    def test_default_time(self):
        time = self.event.time
        self.assertEqual(time, None)

    def test_default_field_name(self):
        fn = self.event.field_name
        self.assertEqual(fn, None)

    def test_default_field_value(self):
        fv = self.event.field_value
        self.assertEqual(fv, None)

class AccessorTest(EventTest):
    def test_get_set_time1(self):
        set_time = datetime(2014, 1, 1, 1, 1)
        self.event.time = set_time
        get_time = self.event.time
        self.assertEqual(
            set_time, get_time,
            "time from get differs from time from set")

    def test_get_set_time2(self):
        set_time = datetime(1, 2, 3, 4, 5, 6)
        self.event.time = set_time
        get_time = self.event.time
        self.assertEqual(
            set_time, get_time,
            "time from get differs from time from set")
        
    def test_get_set_time3(self):
        set_time = datetime(1, 2, 3, 4, 5, 6, 7)
        self.event.time = set_time
        get_time = self.event.time
        self.assertEqual(
            set_time, get_time,
            "time from get differs from time from set")
        
    def set_time(self, time):
        self.event.time = time

    def test_set_time_bad_type1(self):
        set_time = None
        self.assertRaises(
            AssertionError, self.set_time, set_time)

    def test_set_time_bad_type2(self):
        set_time = time.localtime()
        self.assertRaises(
            AssertionError, self.set_time, set_time)

    def test_set_time_bad_type3(self):
        set_time = "2014-08-07 12:12:12"
        self.assertRaises(
            AssertionError, self.set_time, set_time)

    def test_get_set_field_name1(self):
        set_fn = ""
        self.event.field_name = set_fn
        get_fn = self.event.field_name
        self.assertEqual(
            set_fn, get_fn,
            "set value " + str(set_fn) + 
            " differs from get value " + str(get_fn))

    def test_get_set_field_name2(self):
        set_fn = "field name test 2"
        self.event.field_name = set_fn
        get_fn = self.event.field_name
        self.assertEqual(
            set_fn, get_fn,
            "set value " + str(set_fn) + 
            " differs from get value " + str(get_fn))

    def test_get_set_field_name3(self):
        set_fn = "really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really long field name"
        self.event.field_name = set_fn
        get_fn = self.event.field_name
        self.assertEqual(
            set_fn, get_fn,
            "set value " + str(set_fn) + 
            " differs from get value " + str(get_fn))

    def set_field_name(self, name):
        self.event.field_name = name

    def test_set_field_name_bad_type1(self):
        set_name = None
        self.assertRaises(
            AssertionError, self.set_field_name, set_name)

    def test_set_field_name_bad_type2(self):
        set_name = 1234
        self.assertRaises(
            AssertionError, self.set_field_name, set_name)

    def test_set_field_name_bad_type3(self):
        set_name = ["list of", "field_names"]
        self.assertRaises(
            AssertionError, self.set_field_name, set_name) 

    def test_get_set_field_value_int1(self):
        set_field_value = 0
        self.event.field_value = set_field_value
        get_field_value = self.event.field_value
        self.assertEqual(
            set_field_value, get_field_value,
            "field_value from get differs from field_value from set")
    
    def test_get_set_field_value_int2(self):
        set_field_value = 1
        self.event.field_value = set_field_value
        get_field_value = self.event.field_value
        self.assertEqual(
            set_field_value, get_field_value,
            "field_value from get differs from field_value from set")

    def test_get_set_field_value_int3(self):
        set_field_value = 1000000123093210321931209123
        self.event.field_value = set_field_value
        get_field_value = self.event.field_value
        self.assertEqual(
            set_field_value, get_field_value,
            "field_value from get differs from field_value from set")

    def test_get_set_field_value_int4(self):
        set_field_value = -1000000123093210321931209123
        self.event.field_value = set_field_value
        get_field_value = self.event.field_value
        self.assertEqual(
            set_field_value, get_field_value,
            "field_value from get differs from field_value from set")
    
    def test_get_set_field_value_float1(self):
        set_field_value = 0.1
        self.event.field_value = set_field_value
        get_field_value = self.event.field_value
        self.assertEqual(
            set_field_value, get_field_value,
            "field_value from get differs from field_value from set")

    def test_get_set_field_value_float2(self):
        set_field_value = 1.2
        self.event.field_value = set_field_value
        get_field_value = self.event.field_value
        self.assertEqual(
            set_field_value, get_field_value,
            "field_value from get differs from field_value from set")

    def test_get_set_field_value_float3(self):
        set_field_value = 12039124219411.23213142
        self.event.field_value = set_field_value
        get_field_value = self.event.field_value
        self.assertEqual(
            set_field_value, get_field_value,
            "field_value from get differs from field_value from set")

    def test_get_set_field_value_float1(self):
        set_field_value = -12039210412.124123
        self.event.field_value = set_field_value
        get_field_value = self.event.field_value
        self.assertEqual(
            set_field_value, get_field_value,
            "field_value from get differs from field_value from set")

    def test_set_field_value_str1(self):
        set_field_value = ""
        self.event.field_value = set_field_value
        get_field_value = self.event.field_value
        self.assertEqual(
            set_field_value, get_field_value,
            "field_value from get differs from field_value from set")

    def test_set_field_value_str2(self):
        set_field_value = "test set field value str2"
        self.event.field_value = set_field_value
        get_field_value = self.event.field_value
        self.assertEqual(
            set_field_value, get_field_value,
            "field_value from get differs from field_value from set")

    def test_set_field_value_str3(self):
        set_field_value = "really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really long field value"
        self.event.field_value = set_field_value
        get_field_value = self.event.field_value
        self.assertEqual(
            set_field_value, get_field_value,
            "field_value from get differs from field_value from set")
