from bin.models.exceptions import AlarmInactiveException

from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

from datetime import datetime

class Alarm(Base):
    """ Alarm class for the system, usually invoked when readings are 
    gathered that violate system expectations

    Attributes:
    id: id of this alarm assigned by the ORM
    start_time: the time that this alarm began
    end_time: the time that this alarm ended
    reading_id: the id of the reading that caused this alarm
    reading: the reading that caused this alarm
    expectation_id: the id of the expectation that was violated and 
    started the alarm
    expectation: the expectationt that was violated and started this 
    alarm
    """
    __tablename__ = 'alarm'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, default=datetime.now())
    end_time = Column(DateTime)

    reading_id = Column(Integer, ForeignKey('reading.id'))
    reading = relationship("Reading")

    expectation_id = Column(Integer, ForeignKey('expectation.id'))
    expectation = relationship("Expectation")

    quantitative_property_id = Column(Integer, 
                                      ForeignKey('quantitative_property.id'))
    
    def __init__(self, reading=None, expectation=None, start_time=None):
        self.start_time = start_time if start_time else datetime.now()

        self.reading = reading
        self.expectation = expectation

    def __repr__(self):
        return "Alarm(id={}, start_time={}, end_time={}, reading_id={}, expectation_id={}".format(self.id, self.start_time, self.end_time, self.reading_id, self.expectation_id)

    def active(self):
        """ Whether this alarm is active or not (i.e. has an end time or 
        not)
        """ 
        return self.start_time is not None and self.end_time is None

    def end(self):
        """End this alarm (i.e. set its end time to now). If this alarm
        is not active, raises AlarmInactiveException
        """
        if self.end_time is None:
            self.end_time = datetime.now()
        else:
            raise AlarmInactiveException

    def cause(self):
        """The reading that set this alarm off
        """
        return self.reading
