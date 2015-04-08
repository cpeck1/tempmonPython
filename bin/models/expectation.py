from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

class Expectation(Base):
    """Class representing an expectation for some measurement, 
    consisting of an expected range and expected units.
    
    Attributes:
    units: The units of the measurement expected
    low: the low end of the measurement expected
    high: the high end of the measurement expected
    """
    __tablename__ = 'expectation'

    id = Column(Integer, primary_key=True)
    units = Column(String)
    low = Column(Float)
    high = Column(Float)

    def __repr__(self):
        return "Expectation(id={}, units={}, low={}, high={})".format(
            self.id,
            self.units,
            self.low,
            self.high
        )

    def violated_by(self, reading):
        """Whether the given measurement (reading) violates this 
        expectation

        Arguments:
        reading: the measurement being tested
        """
        return ((reading.units != self.units) or 
                not (self.low <= reading.value <= self.high))
