from datetime import datetime
import time

class Alarm:
    """
    Class for an alarm resulting from something not working as anticipated or
    some condition failing.
    """
    def __init__(
            self, container_id, cause = None, start_time = None, 
            last_refresh_time = None, end_time = None):
        assert (isinstance(container_id, int))

        self._container_id = container_id
        self._cause = ''
        self._start_time = None
        self._last_refresh_time = None
        self._end_time = None

        # note all preconditions are handled by setters
        if start_time is not None:
            self.start_time = start_time
        if last_refresh_time is not None:
            self.last_refresh_time = last_refresh_time
        if end_time is not None:
            self.end_time = end_time
        if cause is not None:
            self.cause = cause

    @property
    def container_id(self):
        """
        get this alarm's container id. Note this has no associated setter as 
        this ought to remain constant after initialization
        """
        return self._container_id

    @property
    def cause(self):
        """
        get the cause that this alarm started
        
        >>> Alarm = Alarm()
        >>> alarm.cause
        ''

        >>> alarm.cause = "Jim needs to get potato salad"
        >>> alarm.cause
        'Jim needs to get potato salad'
        """
        
        return self._cause

    @cause.setter
    def cause(self, cause):
        """
        set the cause that this alarm started. 

        >>> alarm = Alarm()
        >>> alarm.cause
        ''

        >>> alarm.cause = "Jim is bringing the potato salad"
        >>> alarm.cause
        'Jim is bringing the potato salad'

        >>> alarm.cause = ["Jim will be here soon", "I want potato salad"]
        Traceback (most recent call last):
        ...
        AssertionError: cause for alarm must be a string
        """
        # precondition: cause must be of type string
        assert isinstance(cause, str), "cause for alarm must be a string"
        self._cause = cause

    @property
    def start_time(self):
        """
        get this alarm's start time

        >>> alarm = Alarm()

        >>> dt1 = datetime(2014, 9, 4, 10, 54)
        >>> alarm.start_time = dt1
        >>> alarm.start_time == dt1
        True
        """
        return self._start_time
        
    @start_time.setter
    def start_time(self, time):
        """
        set this alarm's start time. time must be of type datetime

        >>> alarm = Alarm()
        >>> alarm.start_time = datetime.now()

        >>> alarm.start_time = datetime(2014, 9, 4, 10, 54)
        >>> alarm.start_time = datetime(2014, 9, 4, 10, 54, 12)
        >>> alarm.start_time = datetime(2014, 9, 4, 10, 54, 22, 54)
        
        >>> alarm.start_time = "2014-09-04 10:54:00"
        Traceback (most recent call last):
        ...
        AssertionError: only times of type datetime accepted
        """
        # precondition: time must be of type datetime. If someone wants to 
        # implement string parsing for dates they should obviously do it 
        # elsewhere and convert before passing here
        assert isinstance(time, datetime),"only times of type datetime accepted"

        self._start_time = time

    @property
    def last_refresh_time(self):
        """
        get the last refresh time for this alarm

        >>> alarm = Alarm()
        >>> alarm.last_refresh_time # None

        >>> dt = datetime(2014, 9, 4, 10, 54)
        >>> alarm.last_refresh_time = dt
        >>> alarm.last_refresh_time == dt
        True
        """
        return self._last_refresh_time

    @last_refresh_time.setter
    def last_refresh_time(self, time):
        """
        set the last refresh time for this alarm

        >>> alarm = Alarm()

        >>> alarm.last_refresh_time = datetime(2014, 9, 4, 10, 54)
        >>> alarm.last_refresh_time = datetime(2014, 9, 4, 10, 54, 12)
        >>> alarm.last_refresh_time = datetime(2014, 9, 4, 10, 54, 12, 45)
    
        >>> alarm.last_refresh_time = "2014-09-04 15:04:31"
        Traceback (most recent call last):
        ...
        AssertionError: only times of type datetime accepted
        """
        assert isinstance(time, datetime),"only times of type datetime accepted"

        self._last_refresh_time = time

    @property
    def end_time(self):
        """
        get this alarm's end time.

        >>> alarm = Alarm()
        >>> alarm.end_time # None

        >>> dt1 = datetime(2014, 9, 4, 10, 54)
        >>> alarm.end_time = dt1
        >>> alarm.end_time == dt1
        True
        """
        return self._end_time
    
    @end_time.setter
    def end_time(self, time):
        """
        set this alarm's end time
       
        >>> alarm = Alarm()
        >>> alarm.start_time = datetime.now()

        >>> alarm.start_time = "2014-09-04 10:54:00"
        Traceback (most recent call last):
        ...
        AssertionError: only times of type datetime accepted
        """
        # precondition: time must be of type datetime
        assert isinstance(time, datetime),"only times of type datetime accepted"

        self._end_time = time

    def activate(self, cause):
        """
        start this alarm by setting the start time to now. 

        >>> alarm = Alarm()

        >>> alarm.activate()
        Traceback (most recent call last):
        ...
        TypeError: activate() takes exactly 2 arguments (1 given)

        >>> alarm.activate("Jim brought too much potato salad")
        >>> alarm.start_time is None
        False
        >>> alarm.end_time is None
        True

        >>> alarm.activate("why is there so much potato salad?")
        Traceback (most recent call last):
        ...
        AssertionError: alarm already active
        """
        # precondition: the alarm must not already have started (have a start 
        # time)
        assert self.start_time is None, "alarm already active"

        self.cause = cause
        
        now = datetime.now()
        self.start_time = now
        self.last_refresh_time = now

    def refresh(self):
        """
        Refresh the alarm by setting its last refresh time to now. 

        >>> alarm = Alarm()
        >>> alarm.refresh()
        Traceback (most recent call last):
        ...
        AssertionError: cannot refresh inactive alarms

        >>> alarm.activate("running out of potato-salad related emergencies")
        >>> alarm.refresh() # no return value

        >>> alarm.end()
        >>> alarm.refresh()
        Traceback (most recent call last):
        ...
        AssertionError: cannot refresh inactive alarms
        """
        assert self.is_going_off(),"cannot refresh inactive alarms"
        assert not self.has_ended(),"cannot refresh completed alarms"

        now = datetime.now()
        self.last_refresh_time = now

    def end(self):
        """
        finish this alarm by setting the end time to now

        >>> alarm = Alarm()

        >>> alarm.end()
        Traceback (most recent call last):
        ...
        AssertionError: only active alarms may be ended

        >>> alarm.activate("no one can eat this much potato salad")
        >>> alarm.end_time is None
        True
        
        >>> alarm.end()
        >>> alarm.end_time is None
        False

        >>> alarm.end()
        Traceback (most recent call last):
        ...
        AssertionError: only active alarms may be ended
        """
        # precondition: the alarm must not already have ended (have an end time)
        assert self.is_going_off(), "only active alarms may be ended"

        now = datetime.now()
        self.end_time = now


    def is_going_off(self):
        """
        this alarm is going off if there is a start time but no end time
        
        >>> alarm = Alarm()
        >>> alarm.activate("send Jim to get more potato salad")
        >>> alarm.is_going_off()
        True

        >>> alarm.end()
        >>> alarm.is_going_off()
        False
        """
        st = self.start_time
        et = self.end_time

        # if there is no end time then the alarm is still active
        return st is not None and et is None

    def has_ended(self):
        """
        returns whether or not this alarm is finished. 

        >>> alarm = Alarm()
        >>> alarm.activate("now we need more potato salad")
        >>> alarm.has_ended()
        False
        
        >>> alarm.end()
        >>> alarm.has_ended()
        True
        """
        st = self.start_time
        et = self.end_time

        return st is not None and et is not None


if __name__ == "__main__":
    import doctest
    doctest.testmod()
