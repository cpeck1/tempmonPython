from datetime import datetime

from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship 

class _Reading:
    """
    case class for holding data until it can be verified and transferred
    into a proper enclosure
    """
    def __init__(self, units, value, time=None):
        self.units = units
        self.value = value
        self.time = time if time else datetime.now()

    def __repr__(self):
        return "_Reading(units={}, value={}, time={})".format(
            self.units, self.value, self.time
        )

class Reading(Base):
    """Class representing a measurement of some kind.

    Attributes:
    units: the units of the measurement
    value: the value of the measurement
    time: the time at which the measurement was taken
    atmospheric_condition_id: the id of the condition to which this 
    reading belongs
    """
    __tablename__='reading'

    id = Column(Integer, primary_key=True)
    units = Column(String)
    value = Column(Float)
    time = Column(DateTime, default=datetime.now())

    atmospheric_condition_id = Column(Integer, 
                                      ForeignKey('atmospheric_condition.id'))
    
    def __repr__(self):
        return "Reading(id={}, units={}, value={}, time={}, atmospheric_condition_id={}".format(
            self.id,
            self.units,
            self.value,
            self.time,
            self.atmospheric_condition_id
        )
