# append the project bin to the sys search path
import unittest
from unittest.mock import MagicMock
from datetime import datetime
import time

from context import Context
from transmitter import Transmitter
from alarm import Alarm
from event import Event

class ContextTest(unittest.TestCase):
    def setUp(self):
        self.context = Context(12345)

    def tearDown(self):
        self.context = None

class ContextTest2(unittest.TestCase):
    def setUp(self):
        self.context = Context(12345, "test", "test_field", -80, 15)

    def tearDown(self):
        self.context = None

class ContextTransmitterOpenFailure(unittest.TestCase):
    def setUp(self):
        self.context = Context(12345, "nttest", "nttest_field", 0, 0)

        transmitter = ProductionClass()
        transmitter.is_open = MagicMock(return_value=False)
        transmitter.open = MagicMock(return_value=None)
        transmitter.read = MagicMock(return_value=None)
        
        self.context.transmitter = transmitter

    def tearDown(self):
        self.context = None

class ContextTransmitterReadingFailure(unittest.TestCase):
    def setUp(self):
        self.context = Context(12345, "rftest", "rftest_field", 0, 0)
        
        transmitter = ProductionClass()
        transmitter.is_open = MagicMock(return_value=True)
        transmitter.open = MagicMock(return_value=None)
        transmitter.read = MagicMock(return_value=None)
    
    def tearDown(self):
        self.context = None

class ContextTransmitterBadReadings(unittest.TestCase):
    def setUp(self):
        self.context = Context(12345, "brtest", "brtest_field", -80, 15)
        
        transmitter = ProductionClass()
        transmitter.is_open = MagicMock(return_value=True)
        transmitter.open = MagicMock(return_value=None)
        transmitter.read = MagicMock(return_value=-40)

class DefaultUninitializedStateTest(ContextTest):
    def test_default_id(self):
        context_id = self.context.id
        self.assertEqual(
            context_id, 12345,
            "incorrect default value")

    def test_default_name(self):
        name = self.context.name
        self.assertEqual(
            name, '',
            "incorrect default value")

    def test_default_transmitter(self):
        trans = self.context.transmitter
        self.assertEqual(
            trans, None,
            "incorrect default value")

    def test_default_measured_field_name(self):
        measured_field_name = self.context.name
        self.assertEqual(
            measured_field_name, '',
            "incorrect default value")
            
    def test_default_active_alarm(self):
        alarm = self.context.active_alarm
        self.assertEqual(
            alarm, None,
            "incorrect default value")

class AccessorTest(ContextTest):
    def test_get_set_name1(self):
        set_name = ""
        self.context.name = set_name
        get_name = self.context.name
        self.assertEqual(
            set_name, get_name,
            "set value " + str(set_name) + 
            " did not match get value " + str(get_name))

    def test_get_set_name2(self):
        set_name = "test set name 2"
        self.context.name = set_name
        get_name = self.context.name
        self.assertEqual(
            set_name, get_name,
            "set value " + str(set_name) + 
            " did not match get value " + str(get_name))

    def test_get_set_name3(self):
        set_name = "really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really long name"
        self.context.name = set_name
        get_name = self.context.name
        self.assertEqual(
            set_name, get_name,
            "set value " + str(set_name) + 
            " did not match get value " + str(get_name))

    def set_name(self, name):
        self.context.name = name

    def test_set_name_bad_type1(self):
        set_name = None
        self.assertRaises(
            AssertionError, self.set_name, set_name)

    def test_set_name_bad_type2(self):
        set_name = 12345
        self.assertRaises(
            AssertionError, self.set_name, set_name)

    def test_set_name_bad_type3(self):
        set_name = ["list of", "context names"]
        self.assertRaises(
            AssertionError, self.set_name, set_name)

    def test_get_set_measured_field_name1(self):
        set_name = ""
        self.context.measured_field_name = set_name
        get_name = self.context.measured_field_name
        self.assertEqual(
            set_name, get_name,
            "set value " + str(set_name) + 
            " did not match get value " + str(get_name))

    def test_get_set_measured_field_name2(self):
        set_name = "test get set field name 2"
        self.context.measured_field_name = set_name
        get_name = self.context.measured_field_name
        self.assertEqual(
            set_name, get_name,
            "set value " + str(set_name) + 
            " did not match get value " + str(get_name))

    def test_get_set_measured_field_name3(self):
        set_name = "really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really really long field name"
        self.context.measured_field_name = set_name
        get_name = self.context.measured_field_name
        self.assertEqual(
            set_name, get_name,
            "set value " + str(set_name) + 
            " did not match get value " + str(get_name))

    def set_measured_field_name(self, field_name):
        self.context.measured_field_name = field_name

    def test_set_measured_field_name_bad_type1(self):
        set_name = None
        self.assertRaises(
            AssertionError, self.set_measured_field_name, set_name)

    def test_set_measured_field_name_bad_type2(self):
        set_name = 12345
        self.assertRaises(
            AssertionError, self.set_measured_field_name, set_name)
        
    def test_set_measured_field_name_bad_type3(self):
        set_name = ["list of", "field names"]
        self.assertRaises(
            AssertionError, self.set_measured_field_name, set_name)

    def test_get_set_measured_field_expected_value1(self):
        set_value = 0
        self.context.measured_field_expected_value = set_value
        get_value = self.context.measured_field_expected_value
        self.assertEqual(
            set_value, get_value,
            "set value " + str(set_value) + 
            "did not match get value " + str(get_value))

    def test_get_set_measured_field_expected_value2(self):
        set_value = 1
        self.context.measured_field_expected_value = set_value
        get_value = self.context.measured_field_expected_value
        self.assertEqual(
            set_value, get_value,
            "set value " + str(set_value) + 
            "did not match get value " + str(get_value))

    def test_get_set_measured_field_expected_value3(self):
        set_value = 213092142410
        self.context.measured_field_expected_value = set_value
        get_value = self.context.measured_field_expected_value
        self.assertEqual(
            set_value, get_value,
            "set value " + str(set_value) + 
            "did not match get value " + str(get_value))

    def test_get_set_measured_field_expected_value4(self):
        set_value = 0.000123
        self.context.measured_field_expected_value = set_value
        get_value = self.context.measured_field_expected_value
        self.assertEqual(
            set_value, get_value,
            "set value " + str(set_value) + 
            "did not match get value " + str(get_value))

    def test_get_set_measured_field_expected_value5(self):
        set_value = 1.101131
        self.context.measured_field_expected_value = set_value
        get_value = self.context.measured_field_expected_value
        self.assertEqual(
            set_value, get_value,
            "set value " + str(set_value) + 
            "did not match get value " + str(get_value))

    def test_get_set_measured_field_expected_value6(self):
        set_value = 129843243.123912849
        self.context.measured_field_expected_value = set_value
        get_value = self.context.measured_field_expected_value
        self.assertEqual(
            set_value, get_value,
            "set value " + str(set_value) + 
            "did not match get value " + str(get_value))

    def set_measured_field_expected_value(self, val):
        self.context.measured_field_expected_value = val

    def test_set_measured_field_expected_value_bad_type1(self):
        set_value = None
        self.assertRaises(
            AssertionError, self.set_measured_field_expected_value, set_value)

    def test_set_measured_field_expected_value_bad_type2(self):
        set_value = "set value"
        self.assertRaises(
            AssertionError, self.set_measured_field_expected_value, set_value)

    def test_set_measured_field_expected_value_bad_type3(self):
        set_value = [1234, 5678]
        self.assertRaises(
            AssertionError, self.set_measured_field_expected_value, set_value)

    def test_get_set_measured_field_variance1(self):
        set_var = 0
        self.context.measured_field_variance = set_var
        get_var = self.context.measured_field_variance
        self.assertEqual(
            set_var, get_var,
            "set value " + str(set_var) + 
            "did not match get value " + str(get_var))

    def test_get_set_measured_field_variance2(self):
        set_var = 1
        self.context.measured_field_variance = set_var
        get_var = self.context.measured_field_variance
        self.assertEqual(
            set_var, get_var,
            "set value " + str(set_var) + 
            "did not match get value " + str(get_var))

    def test_get_set_measured_field_variance3(self):
        set_var = 985924581032
        self.context.measured_field_variance = set_var
        get_var = self.context.measured_field_variance
        self.assertEqual(
            set_var, get_var,
            "set value " + str(set_var) + 
            "did not match get value " + str(get_var))

    def test_get_set_measured_field_variance4(self):
        set_var = 0.21449341
        self.context.measured_field_variance = set_var
        get_var = self.context.measured_field_variance
        self.assertEqual(
            set_var, get_var,
            "set value " + str(set_var) + 
            "did not match get value " + str(get_var))

    def test_get_set_measured_field_variance5(self):
        set_var = 1.1240945
        self.context.measured_field_variance = set_var
        get_var = self.context.measured_field_variance
        self.assertEqual(
            set_var, get_var,
            "set value " + str(set_var) + 
            "did not match get value " + str(get_var))

    def test_get_set_measured_field_variance6(self):
        set_var = 438532412.12498304
        self.context.measured_field_variance = set_var
        get_var = self.context.measured_field_variance
        self.assertEqual(
            set_var, get_var,
            "set value " + str(set_var) + 
            "did not match get value " + str(get_var))

    def set_measured_field_variance(self, var):
        self.context.measured_field_variance = var

    def test_set_measured_field_variance_bad_type1(self):
        set_var = None
        self.assertRaises(
            AssertionError, self.set_measured_field_variance, set_var)

    def test_set_measured_field_variance_bad_type2(self):
        set_var = "123.456"
        self.assertRaises(
            AssertionError, self.set_measured_field_variance, set_var)
        

    def test_set_measured_field_variance_bad_type3(self):
        set_var = [1234, 5678]
        self.assertRaises(
            AssertionError, self.set_measured_field_variance, set_var)

    def test_get_set_transmitter1(self):
        set_trans = Transmitter(self.context.id)
        self.context.transmitter = set_trans
        get_trans = self.context.transmitter
        self.assertEqual(
            set_trans, get_trans,            
            "set value " + str(set_trans) + 
            " did not match get value " + str(get_trans))

    def test_get_set_transmitter2(self):
        set_trans = Transmitter(self.context.id, 
                                vendor_id=0x1234, product_id=0x4321)
        self.context.transmitter = set_trans
        get_trans = self.context.transmitter
        self.assertEqual(
            set_trans, get_trans,            
            "set value " + str(set_trans) + 
            " did not match get value " + str(get_trans))

    def test_get_set_transmitter3(self):
        set_trans = Transmitter(self.context.id, "Man1", "Name1", 1, 1)
        self.context.transmitter = set_trans
        get_trans = self.context.transmitter
        self.assertEqual(
            set_trans, get_trans,            
            "set value " + str(set_trans) + 
            " did not match get value " + str(get_trans))

    def set_transmitter(self, transmitter):
        self.context.transmitter = transmitter

    def test_set_transmitter_bad_type1(self):
        set_trans = None
        self.assertRaises(
            AssertionError, self.set_transmitter, set_trans)

    def test_set_transmitter_bad_type2(self):
        set_trans = 12345
        self.assertRaises(
            AssertionError, self.set_transmitter, set_trans)

    def test_set_transmitter_bad_type3(self):
        set_trans = Transmitter
        self.assertRaises(
            AssertionError, self.set_transmitter, set_trans)

    def test_get_set_active_alarm1(self):
        set_alarm = Alarm(self.context.id)
        self.context.active_alarm = set_alarm
        get_alarm = self.context.active_alarm
        self.assertEqual(
            set_alarm, get_alarm,
            "set value " + str(set_alarm) + 
            " did not match get value " + str(get_alarm))

    def test_get_set_active_alarm2(self):
        set_alarm = Alarm(self.context.id, "test2")
        self.context.active_alarm = set_alarm
        get_alarm = self.context.active_alarm
        self.assertEqual(
            set_alarm, get_alarm,
            "set value " + str(set_alarm) + 
            " did not match get value " + str(get_alarm))

    def test_get_set_active_alarm3(self):
        set_alarm = Alarm(
            self.context.id, "test3", 
            start_time=datetime.now(), last_refresh_time=datetime.now())
        self.context.active_alarm = set_alarm
        get_alarm = self.context.active_alarm
        self.assertEqual(
            set_alarm, get_alarm,
            "set value " + str(set_alarm) + 
            " did not match get value " + str(get_alarm))

    def set_active_alarm(self, alarm):
        self.context.active_alarm = alarm

    def test_set_active_alarm_bad_type1(self):
        set_alarm = None
        self.assertRaises(
            AssertionError, self.set_active_alarm, set_alarm)

    def test_set_active_alarm_bad_type2(self):
        set_alarm = 12345
        self.assertRaises(
            AssertionError, self.set_active_alarm, set_alarm)

    def test_set_active_alarm_bad_type3(self):
        set_alarm = Alarm
        self.assertRaises(
            AssertionError, self.set_active_alarm, set_alarm)

    def test_get_set_last_event1(self):
        set_event = Event(12345)
        self.context.last_event = set_event
        get_event = self.context.last_event
        self.assertEqual(
            set_event, get_event,
            "set value " + str(set_event) + 
            " did not match get value " + str(get_event))
        
    def test_get_set_last_event2(self):
        set_event = Event(12345, datetime.now())
        self.context.last_event = set_event
        get_event = self.context.last_event
        self.assertEqual(
            set_event, get_event,
            "set value " + str(set_event) + 
            " did not match get value " + str(get_event))

    def test_get_set_last_event3(self):
        set_event = Event(12345, datetime.now(), "test", 90931)
        self.context.last_event = set_event
        get_event = self.context.last_event
        self.assertEqual(
            set_event, get_event,
            "set value " + str(set_event) + 
            " did not match get value " + str(get_event))

    def set_last_event(self, event):
        self.context.last_event = event

    def test_set_last_event_bad_type1(self):
        set_event = None
        self.assertRaises(
            AssertionError, self.set_last_event, set_event)
        
    def test_set_last_event_bad_type2(self):
        set_event = 1234
        self.assertRaises(
            AssertionError, self.set_last_event, set_event)
        
    def test_set_last_event_bad_type3(self):
        set_event = "string event!"
        self.assertRaises(
            AssertionError, self.set_last_event, set_event)

class ReadingOutOfRangeTest(ContextTest2):
    def test_range1(self):
        r = 0
        self.assertTrue(
            self.context.reading_out_of_range(r)) 

    def test_range2(self):
        r = -50
        self.assertTrue(
            self.context.reading_out_of_range(r)) 

    def test_range3(self):
        r = 123.1245
        self.assertTrue(
            self.context.reading_out_of_range(r)) 

    def test_range4(self):
        r = -64.9999999
        self.assertTrue(
            self.context.reading_out_of_range(r)) 

    def test_range5(self):
        r = -95.000001
        self.assertTrue(
            self.context.reading_out_of_range(r)) 

class TestActivateAlarm(ContextTest2):
    def test_activate_alarm1(self):
        cause = "transmitter failed to open"
        self.context.activate_alarm(cause)
        alarm = self.context.active_alarm
        self.assertTrue(
            alarm is not None and alarm.is_going_off(),
            "should have resulted in an active alarm for the context")

    def test_activate_alarm2(self):
        cause = "transmitter failed to gather reading"
        self.context.activate_alarm(cause)
        alarm = self.context.active_alarm
        self.assertTrue(
            alarm is not None and alarm.is_going_off(),
            "should have resulted in an active alarm for the context")

    def test_activate_alarm3(self):
        reading = -55.0
        cause = "transmitter gathered reading out of acceptable range"
        self.context.activate_alarm(cause, reading)
        alarm = self.context.active_alarm
        self.assertTrue(
            alarm is not None and alarm.is_going_off(),
            "should have resulted in an active alarm for the context")
        
class TestAddEvent(ContextTest2):
    def test_add_event1(self):
        # note add event isn't responsible for checking if the given reading is
        # above or below a certain range; this is left to functions that will
        # invoke add_event
        reading = 0
        self.context.add_event(reading)
        last_event = self.context.last_event
        self.assertTrue(last_event is not None,
            "last_event wasn't even set")
        self.assertEqual(
            last_event.field_value, reading,
            "did not match expected value")

    def test_add_event1(self):
        reading = 123
        self.context.add_event(reading)
        last_event = self.context.last_event
        self.assertTrue(
            last_event is not None,
            "last_event wasn't even set")
        self.assertEqual(
            last_event.field_value, reading,
            "did not match expected value")

    def test_add_event1(self):
        reading = 123.56789
        self.context.add_event(reading)
        last_event = self.context.last_event
        self.assertTrue(last_event is not None,
                        "last_event wasn't even set")
        self.assertEqual(
            last_event.field_value, reading,
            "did not match expected value")
