# append the project bin to the sys search path
import sys
sys.path.append("../bin/models")
sys.path.append("./bin/models")

import unittest
from unittest.mock import MagicMock
from datetime import datetime
import time
from context import Context
from transmitter import Transmitter
from alarm_specification import AlarmSpecification
from alarm import Alarm

class ContextTest(unittest.TestCase):
    def setUp(self):
        self.context = Context(12345)

    def tearDown(self):
        self.context = None

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
            
    def test_default_alarm_specification(self):
        alarm_specification = self.context.alarm_specification
        self.assertEqual(
            alarm_specification, None,
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

    def test_get_set_alarm_specification1(self):
        pass

    def test_get_set_alarm_specification2(self):
        pass

    def test_get_set_alarm_specification3(self):
        pass

    def set_alarm_specification(self, spec):
        self.context.alarm_specification = spec

    def test_set_alarm_specificaiton_bad_type1(self):
        set_alarm_spec = None
        self.assertRaises(
            AssertionError, self.set_alarm_specification, set_alarm_spec)

    def test_set_alarm_specificaiton_bad_type2(self):
        set_alarm_spec = [lambda r: r in range(0, 100), lambda r: r is not None]
        self.assertRaises(
            AssertionError, self.set_alarm_specification, set_alarm_spec)

    def test_set_alarm_specificaiton_bad_type3(self):
        set_alarm_spec = Alarm(12345)
        self.assertRaises(
            AssertionError, self.set_alarm_specification, set_alarm_spec)

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

class ActivateAlarmTest(ContextTest):
    def test_activate_alarm1(self):
        # class: overdue reading
        pass

    def test_activate_alarm2(self):
        # class: transmitter error
        pass

    def test_activate_alarm3(self):
        # class: reading failed
        pass

    def test_activate_alarm4(self):
        # class: bad reading
        pass

    def test_activate_alarm5(self):
        # class: TBD
        pass

    def test_activate_alarm6(self):
        # class: TBD
        pass
