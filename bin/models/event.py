from datetime import datetime

class Event:
    """
    class representing a temperature reading for an associated container
    """
    
    def __init__(
            self, context_id, time=None, field_name=None, 
            field_value=None, status=None):
        assert (isinstance(context_id, int))

        self._context_id = context_id
        self._time = None
        self._field_name = None
        self._field_value = None

        # typechecking is left to setter functions
        if time is not None:
            self.time = time
        if field_name is not None:
            self.field_name = field_value
        if field_value is not None:
            self.field_value = field_value
    
    @property
    def context_id(self):
        """
        get this event's associated context's id

        >>> event = Event(12345)
        >>> event.context_id
        12345
        """
        return self._context_id
    
    @property
    def time(self):
        """
        return the time that this event was recorded

        >>> event = Event(12345)
        >>> time = datetime.now()
        >>> event.time = time
        >>> event.time == time
        True
        """
        return self._time

    @time.setter
    def time(self, time):
        """
        set the time that this event was recorded

        ***time must be of type datetime***

        >>> event = Event(12345)
        >>> time = datetime.now()
        >>> event.time = time
        
        >>> event.time = "2014-08-06 12:13:43"
        Traceback (most recent call last):
        ...
        AssertionError: expected <type 'datetime.datetime'>, got <type 'str'>
        """
        assert isinstance(time, datetime), \
            "expected <type 'datetime.datetime'>, got "+str(type(time))

        self._time = time

    @property
    def field_name(self):
        """
        get this event's recorded field_name

        Usage:
        >>> event = Event(12345, field_name="test1")
        >>> event.field_name
        'test1'
        """
        return self._field_name

    @field_name.setter
    def field_name(self, field_name):
        """
        set this event's field_name. 

        *** Field name must be of type str ***

        Usage:
        >>> event = Event(12345, fiend_name="test2")
        >>> event.field_name = "test3"
        >>> event.field_name
        'test3'

        >>> event.field_name = 123
        Traceback (most recent call last):
        ...
        AssertionError: expected <type 'str'> but got <type 'int'>
        """
        assert isinstance(field_name, str),\
            "expected <type 'str'> but got " + str(type(field_name)) 

        self._field_name = field_name

    @property
    def field_value(self):
        """
        get this event's recorded field_value
        
        >>> event = Event(12345)
        >>> field_value = -80.1
        >>> event.field_value = field_value
        
        >>> event.field_value
        -80.1
        """
        return self._field_value
        
    @field_value.setter
    def field_value(self, temp):
        """
        set the field_value of this event 

        field value may be of any type

        >>> event = Event(12345, field_value = 80)
        >>> event.field_value = -81.5
        >>> event.field_value
        -81.5

        >>> event.field_value = "-84.5"
        Traceback (most recent call last):
        ...
        AssertionError: expected <type 'int'> or <type 'float'>, got <type 'str'>
        """
        self._field_value = temp
