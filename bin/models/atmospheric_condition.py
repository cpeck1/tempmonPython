from datetime import datetime, timedelta

from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

from bin.models.alarm import Alarm
from bin.models.reading import Reading, _Reading

class AtmosphericCondition(Base):
    """An atmospheric condition of an environment, for example 
    temperature

    Attributes:
    id: the id of this atmospheric condition assigned by the ORM
    type: the classification of this atmospheric condition, e.g. 
    temperature, relative humidity, atmospheric pressure etc
    channel_bus: the USB bus of the transmitter channel responsible for 
    monitoring this condition
    channel_address: the USB bus address of the transmitter channel 
    responsible for monitoring this condition
    channel_number: the channel number of the transmitter channel 
    responsible for monitoring this condition
    """
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

        self.expectation = expectation

    def __repr__(self):
        return "AtmosphericCondition(id={}, type={}, channel_bus={}, channel_address={}, channel_number={}, recording_frequency={}, expectation={})".format(
            self.id, 
            self.type, 
            self.channel_bus, 
            self.channel_address, 
            self.channel_number,
            self._recording_frequency,
            self.expectation
        )

    @property
    def recording_frequency(self):
        return timedelta(0, self._recording_frequency, 0) 
                
    @recording_frequency.setter
    def recording_frequency(self, value):
        self._recording_frequency = value

    def read_channel(self): 
        return _Reading(value=self.channel.read(), units=self.channel.units)

    def most_recent_reading(self):
        try:
            return self.readings[-1]
        except IndexError:
            return None

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
            last_reading = self.most_recent_reading()
            return (datetime.now()-last_reading.time)>self.recording_frequency
        except AttributeError:
            return True
