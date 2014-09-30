from transmitter import Transmitter
from alarm import Alarm
from event import Event
from datetime import datetime

class Context:
    """
    the context in which some kind of reading is measured
    """
    def __init__(
            self, context_id, context_name=None, measured_field_name=None,
            measured_field_expected_value=None, measured_field_variance=None):
        self._id = context_id

        self._name = ''

        self._measured_field_name = ''
        self._measured_field_expected_value = None
        self._measured_field_variance = None

        self._transmitter = None
        self._last_event = None
        self._active_alarm = None

        if context_name is not None:
            self.name = context_name
        if measured_field_name is not None:
            self.measured_field_name = measured_field_name
        if measured_field_expected_value is not None:
            self.measured_field_expected_value = measured_field_expected_value
        if measured_field_variance is not None:
            self.measured_field_variance = measured_field_variance 

    @property
    def id(self):
        """
        return this context's id
        
        Usage:
        >>> c = Context(12345)
        >>> c.id
        12345
        """
        return self._id

    @property
    def name(self):
        """
        return this context's name

        Usage:
        >>> c = Context(12345, 'Test context')
        >>> c.name
        'Test context'
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        set this context's name

        *** name must be of type str ***

        >>> Usage:
        >>> c = Context(12345, 'test1')
        >>> c.name = 'test2'
        >>> c.name
        'test2'
        >>> c.name = 12345
        Traceback (most recent call last):
        ...
        AssertionError: expected <type 'str'> but got <type 'int'>
        """
        assert isinstance(name, str),\
            "expected <type 'str'> but got " + str(type(name))

        self._name = name


    @property
    def measured_field_name(self):
        """
        get the name of the field that this context is monitoring

        Usage:
        >>> c = Context(12345, measured_field_name='test')
        >>> c.measured_field_name
        'test'
        """
        return self._measured_field_name

    @measured_field_name.setter
    def measured_field_name(self, field_name):
        """
        set the name of the field that this context is monitoring

        Usage:
        >>> c = Context(12345, measured_field_name='test1')
        >>> c.measured_field_name = 'test2'
        >>> c.measured_field_name
        'test2'
        >>> c.measured_field_name = 12345
        Traceback (most recent call last):
        ...
        AssertionError: expected <type 'str'> but got <type 'int'>
        """
        assert isinstance(field_name, str),\
            "expected <type 'str'> but got " + str(type(field_name))

        self._measured_field_name = field_name

    @property
    def measured_field_expected_value(self):
        """
        get the value this context expects its measured field to be
        
        Usage:
        >>> ctx = Context(12345, measured_field_expected_value=-80)
        >>> ctx.measured_field_expected_value
        -80
        """
        return self._measured_field_expected_value

    @measured_field_expected_value.setter
    def measured_field_expected_value(self, value):
        """
        set the value that this context expects its measured field to be. The
        given value must be numeric as when used in tandem with variance a
        subtraction method is invoked.

        *** value must be of type int or float ***

        >>> ctx = Context(12345, measured_field_expected_value=-80)
        >>> ctx.measured_field_expected_value = 40
        >>> ctx.measured_field_expected_value
        40

        >>> ctx.measured_field_expected_value = "12345"
        Traceback (most recent call last):
        ...
        AssertionError: expected <type 'int'> or <type 'float'> but got <type 'str'>
        """
        assert (isinstance(value, int) or isinstance(value, float)),\
            "expected <type 'int'> or <type 'float'> but got "+str(type(value))

        self._measured_field_expected_value = value
    
    @property
    def measured_field_variance(self):
        """
        get the variance of this context's measured field. This with 
        measured_field_expected_value creates a range of:

        [measured_field_expected_value - measured_field_variance,
         measured_field_expected_value + measured_field_variance]

        Usage:
        >>> ctx = Context(12345, measured_field_variance=20)
        >>> ctx.measured_field_variance
        20
        """
        return self._measured_field_variance

    @measured_field_variance.setter
    def measured_field_variance(self, var):
        """
        set the acceptable variance of this context's measured field. Similarly
        to expected_value, since this property is involved in a subtraction
        operation variance should be of type int or float.

        *** variance must be of type int or float ***

        >>> ctx = Context(12345, measured_vield_variance=20)
        >>> ctx.measured_field_variance = 100
        >>> ctx.measured_field_variance
        100

        >>> ctx.measured_field_variance = "alot"
        Traceback (most recent call last):
        ...
        AssertionError: expected <type 'int'> or <type 'float'> but got <type 'str'>
        """
        assert (isinstance(var, int) or isinstance(var, float)),\
            "expected <type 'int'> or <type 'float'> but got " + str(type(var))
            
        self._measured_field_variance = var
    
    @property
    def transmitter(self):
        """
        get the transmitter assigned to this context

        Usage:
        >>> c = Context(12345)
        >>> trans = Transmitter(c.id, 'man1')
        >>> c.transmitter = trans
        >>> c.transmitter.manufacturer
        'man1'
        """
        return self._transmitter

    @transmitter.setter
    def transmitter(self, transmitter):
        """
        set the transmitter assigned to this context

        *** transmitter must be a transmitter object ***

        Usage:
        >>> c = Context(12345)
        >>> c.transmitter = Context(12345)

        Traceback (most recent call last):
        ...
        AssertionError: expected <class 'transmitter.Transmitter'> got <class 'context.Context'>
        """
        assert isinstance(transmitter, Transmitter),\
            "expected <class 'transmitter.Transmitter'> got "+\
            str(type(transmitter))
        
        self._transmitter = transmitter

    @property
    def last_event(self):
        """
        get the last event committed by this context

        Usage:
        >>> ctx = Context(12345)
        >>> ctx.add_event(-60)
        >>> ctx.last_event.field_value
        -60
        """
        return self._last_event

    @last_event.setter
    def last_event(self, event):
        """
        set the event to the last event committed by this context

        *** event must be of class Event ***

        Usage (this is mostly for other functions, don't use this function to 
        set the last event, use add_event instead):
        >>> ctx = Context(12345)
        >>> e = Event(ctx.id, field_value=60.0)
        >>> ctx.last_event = e
        >>> ctx.last_event.field_value
        60.0

        >>> ctx.last_event = -50
        Traceback (most recent call last):
        ...
        AssertionError: expected <class 'event.Event'> but got <type 'int'>
        """
        assert isinstance(event, Event),\
            "expected <class 'event.Event'> but got "+str(type(event))

        self._last_event = event

    @property
    def active_alarm(self):
        """
        get the active alarm for this context

        Usage:
        >>> c = Context(12345)
        >>> c.active_alarm = Alarm(c.id)
        >>> isinstance(c.active_alarm, Alarm)
        True
        """
        return self._active_alarm

    @active_alarm.setter
    def active_alarm(self, alarm):
        """
        set the active alarm for this context
        
        Usage:
        >>> c = Context(12345)
        >>> c.set_active_alarm(c)
        Traceback (most recent call last):
        ...
        AssertionError: expected <class 'alarm.Alarm'> but got <class 'context.Context'>
        """
        assert isinstance(alarm, Alarm),\
            "expected "+str(type(Alarm(1234)))+" but got " + str(type(alarm))

        self._active_alarm = alarm

    def reading_out_of_range(self, reading):
        """
        if the reading falls outside the range

        [measured_field_expected_value - measured_field_variance,
         measured_field_expected_value + measured_field_variance]

        then return True, else return False

        Usage:
        >>> ctx = Context(12345, measured_field_expected_value = -80, measured_field_variance = 15)
        >>> ctx.reading_out_of_range(-80)
        False
        >>> ctx.reading_out_of_range(0)
        True
        """
        # opted not to use range() here for the oh so common case that the value
        # lands EXACTLY on the upper bound (ub)
        lb = self.measured_field_expected_value - self.measured_field_variance
        ub = self.measured_field_expected_value + self.measured_field_variance

        return ((reading < lb) or (reading > ub))

    def activate_alarm(self, alarm_category, causer=None):
        """
        spawns a new alarm and assigns it to this context's active alarm. 

        Type assertions are handled by alarm's accessor functions. If a reading
        is given, the reading's value is tacked on to the alarm_cause string

        Usage:
        >>> ctx = Context(12345)
        >>> ctx.activate_alarm("testing has gone horribly wrong!")
        >>> ctx.active_alarm.cause
        'testing has gone horribly wrong!'
        """
        a = Alarm(self.id)
        a.activate(alarm_category)
        self.active_alarm = a

    def add_event(self, reading):
        """
        spawns a new event consisting of the given reading, the time and 
        details about the event found in this context's properties

        Usage:
        >>> ctx = Context(12345)
        >>> ctx.add_event(50)
        >>> ctx.last_event.field_value
        50
        """
        e = Event(self.id, datetime.now(), self.measured_field_name, reading)

        self.last_event = e

    def process_reading(self, reading):
        """
        take the given reading and run it through this context's checks and 
        balances: 
        -If the reading is out of range for this context, activate an
        out-of-range alarm. 
        -If there is no reading to process (i.e. its value is None) activate a 
        reading failed alarm
        -Otherwise add a new event consisting of this reading.
        """
        if self.reading_out_of_range(reading):
            self.activate_alarm("reading out of expected range")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
