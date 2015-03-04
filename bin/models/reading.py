from datetime import datetime

from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship 

class Reading(Base):
    __tablename__='reading'

    id = Column(Integer, primary_key=True)
    units = Column(String)
    value = Column(Float)
    time = Column(DateTime, default=datetime.now())

    atmospheric_condition_id = Column(Integer, 
                                      ForeignKey('atmospheric_condition.id'))

    def __repr__(self):
        return "Reading(units={!r}, value={!r}, time={!r}".format(self.units, self.value, self.time)

    def __str__(self):
        return "Reading: \n\tunits: {!r} \n\tvalue: {!r} \n\ttime: {!s}".format(self.units, self.value, self.time)
