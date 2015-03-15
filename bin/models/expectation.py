from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

# TODO replace with REAL conversion package
class SomeConversionPackage:
    def convert(reading, units):
        # convert reading with properties units and value to given units
        if reading.units == 'Celsius' and units == 'Fahrenheit':
            nv = (reading.value*(9/5)) + 32
            return reading(nv, units)
        elif reading.units == 'Fahrenheit' and units == 'Celsius':
            nv = (reading.value - 32)*(5/9)
            return reading(nv, units)
        else:
            return None

class Expectation(Base):
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
        return ((reading.units != self.units) or 
                not (self.low <= reading.value <= self.high))
