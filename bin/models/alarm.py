from datetime import datetime
import time

class Alarm:
    """
    Class for an alarm resulting from something not working as anticipated or
    some condition failing.
    """
    def __init__(
            self, container_id, cause=None, start_time=None, 
            last_refresh_time=None, end_time=None):
        assert (isinstance(container_id, int))

        self._container_id = container_id
        self._cause = None
        self._start_time = None
        self._last_refresh_time = None
        self._end_time = None

        # note all preconditions are handled by setters
        if cause is not None:
            self.cause = cause
        if start_time is not None:
            self.start_time = start_time
        if last_refresh_time is not None:
            self.last_refresh_time = last_refresh_time
        if end_time is not None:
            self.end_time = end_time

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
        return the cause of the alarm, usually the object that set it off

        Usage:
        >>> a = Alarm(12345, cause=[1,2,3,4])
        >>> a.cause
        [1, 2, 3, 4]
        """
        return self._cause

    @cause.setter
    def cause(self, cause):
        """
        set the cause of the alarm. Accepts any type. Preferably something with
        a nice __str__ method as it will likely be used to describe the alarm 
        later. The cause is also used to classify the alarm: the cause is 
        interpreted from the causing object.
        
        Usage:
        >>> a = Alarm(12345, cause=[1,2,3,4,5])
        >>> a.cause = [2, 3, 4]
        >>> a.cause
        [2, 3, 4]

        >>> a.cause = "abcd"
        >>> a.cause = datetime.now()
        >>> a.cause = alarm #that's right, it caused itself. The Matrix yo
        """
        # no assertions, accepts any type
        self._cause = cause

    @property
    def start_time(self):
        """
        get this alarm's start time

        >>> a = Alarm(12345)

        >>> dt1 = datetime(2014, 9, 4, 10, 54)
        >>> a.start_time = dt1
        >>> a.start_time == dt1
        True
        """
        return self._start_time
        
    @start_time.setter
    def start_time(self, time):
        """
        set this alarm's start time. time must be of type datetime

        >>> a = Alarm(12345)
        >>> a.start_time = datetime.now()

        >>> a.start_time = datetime(2014, 9, 4, 10, 54)
        >>> a.start_time = datetime(2014, 9, 4, 10, 54, 12)
        >>> a.start_time = datetime(2014, 9, 4, 10, 54, 22, 54)
        
        >>> a.start_time = "2014-09-04 10:54:00"
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

        >>> a = Alarm(12345)
        >>> a.last_refresh_time # None

        >>> dt = datetime(2014, 9, 4, 10, 54)
        >>> a.last_refresh_time = dt
        >>> a.last_refresh_time == dt
        True
        """
        return self._last_refresh_time

    @last_refresh_time.setter
    def last_refresh_time(self, time):
        """
        set the last refresh time for this alarm

        >>> a = Alarm(12345)

        >>> a.last_refresh_time = datetime(2014, 9, 4, 10, 54)
        >>> a.last_refresh_time = datetime(2014, 9, 4, 10, 54, 12)
        >>> a.last_refresh_time = datetime(2014, 9, 4, 10, 54, 12, 45)
    
        >>> a.last_refresh_time = "2014-09-04 15:04:31"
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

        >>> a = Alarm(12345)
        >>> a.end_time # None

        >>> dt1 = datetime(2014, 9, 4, 10, 54)
        >>> a.end_time = dt1
        >>> a.end_time == dt1
        True
        """
        return self._end_time
    
    @end_time.setter
    def end_time(self, time):
        """
        set this alarm's end time
       
        >>> a = Alarm(12345)
        >>> a.start_time = datetime.now()

        >>> a.start_time = "2014-09-04 10:54:00"
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

        >>> a = Alarm(12345)
        >>> a.activate()
        Traceback (most recent call last):
        ...
        TypeError: activate() missing 1 required positional argument: 'cause'

        >>> a.activate(cause="Jim brought too much potato salad")
        >>> a.start_time is None
        False
        >>> a.end_time is None
        True

        >>> a.activate("why is there so much potato salad?")
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

        >>> a = Alarm(12345)
        >>> a.refresh()
        Traceback (most recent call last):
        ...
        AssertionError: cannot refresh inactive alarms

        >>> a.activate("running out of potato-salad related emergencies")
        >>> a.refresh() # no return value

        >>> a.end()
        >>> a.refresh()
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

        >>> a = Alarm(12345)

        >>> a.end()
        Traceback (most recent call last):
        ...
        AssertionError: only active alarms may be ended

        >>> a.activate("no one can eat this much potato salad")
        >>> a.end_time is None
        True
        
        >>> a.end()
        >>> a.end_time is None
        False

        >>> a.end()
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
        
        >>> a = Alarm(12345)
        >>> a.activate("send Jim to get more potato salad")
        >>> a.is_going_off()
        True

        >>> a.end()
        >>> a.is_going_off()
        False
        """
        st = self.start_time
        et = self.end_time

        # if there is no end time then the alarm is still active
        return st is not None and et is None

    def has_ended(self):
        """
        returns whether or not this alarm is finished. 

        >>> a = Alarm(12345)
        >>> a.activate("now we need more potato salad")
        >>> a.has_ended()
        False
        
        >>> a.end()
        >>> a.has_ended()
        True
        """
        st = self.start_time
        et = self.end_time

        return st is not None and et is not None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
