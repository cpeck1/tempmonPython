from datetime import datetime, timedelta

from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

from .alarm import Alarm
from .reading import Reading

class AtmosphericCondition(Base):
    __tablename__ = 'atmospheric_condition'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    channel_bus = Column(Integer)
    channel_address = Column(Integer)
    channel_number = Column(Integer)

    channel = None

    _recording_frequency = Column(Integer) # better way of storing needed
    environment_id = Column(Integer, ForeignKey('environment.id'))

    # Many-to-one relationship with expectation
    expectation_id = Column(Integer, ForeignKey('expectation.id'))
    expectation = relationship("Expectation",
                               backref='atmospheric_condition',
                               uselist=False)
    # One-to-many relationship with readings
    readings = relationship("Reading",
                            backref='atmospheric_condition',
                            cascade="all, delete, delete-orphan")
    # One-to-many relationship with alarms
    alarms = relationship("Alarm",
                          backref='atmospheric_condition',
                          cascade="all, delete, delete-orphan")

    def __init__(
            self,
            type,
            channel_bus,
            channel_address,
            channel_number,
            rec_freq,
            expectation
    ):
        self.type = type
        self.channel_bus = channel_bus
        self.channel_address = channel_address
        self.channel_number = channel_number
        self._recording_frequency = rec_freq

        self.channel = None

        self.environment_id = None
        self.expectation_id = expectation.id
        self.expectation = expectation
        self.readings = []
        self.alarms = []

    @property
    def recording_frequency(self):
        return timedelta(0, self._recording_frequency, 0) 
                
    @recording_frequency.setter
    def recording_frequency(self, value):
        self._recording_frequency = value

    def read_channel(self): 
        return Reading(value=self.channel.read(), units=self.channel.units)

    def most_recent_alarm(self):
        try:
            return self.alarms[-1]
        except IndexError:
            return None

    def alarm_active(self):
        if self.most_recent_alarm() is None: return False

        return self.most_recent_alarm().active()

    def record_due(self):
        try:
            last_reading = self.readings[-1]
            return (datetime.now()-last_reading.time)>self.recording_frequency
        except IndexError:
            return True
