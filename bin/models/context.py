from transmitter import Transmitter
from alarm import Alarm
from alarm_specification import AlarmSpecification
class Context:
    """
    the context in which some kind of reading is measured
    """
    def __init__(self, context_id, context_name=None, measured_field_name=None):
        self._id = context_id

        self._name = ''

        self._measured_field_name = ''
        self._transmitter = None
        self._alarm_specification = None
        self._active_alarm = None

        if context_name is not None:
            self.name = context_name
        if measured_field_name is not None:
            self.measured_field_name = measured_field_name
    
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
        AssertionError: expected <class 'transmitter.Transmitter'>, got <class 'context.Context'>
        """
        assert isinstance(transmitter, Transmitter),\
            "expected <class 'transmitter.Transmitter'> got "+\
            str(type(transmitter))
        
        self._transmitter = transmitter

    @property
    def alarm_specification(self): 
        """
        get this context's alarm specifications        
        """
        return self._alarm_specification

    @alarm_specification.setter
    def alarm_specification(self, specification):
        assert isinstance(specification, AlarmSpecification),\
            "expected <class 'alarm_specification.AlarmSpecification> " +\
            "but got " + str(type(specification))

        self._alarm_specification = specification

    @property
    def active_alarm(self):
        """
        get the active alarm for this context

        Usage:
        >>> c = Context(12345)
        >>> c.set_active_alarm(Alarm(c.get_id()))
        >>> isinstance(c.get_active_alarm(), Alarm)
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
            "expected <class 'alarm.Alarm'> but got " + str(type(alarm))

        self._active_alarm = alarm

    def activate_alarm(self, alarm_class, reading=None):
        """
        spawns a new alarm and assigns it to this context's active alarm. 
        """
        pass

    def add_event(self, reading):
        """
        spawns a new event consisting of the given reading, the time and 
        details about the event found in this context's properties
        """
        pass
