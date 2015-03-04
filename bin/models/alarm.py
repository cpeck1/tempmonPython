from .exceptions import AlarmInactiveException

from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

from datetime import datetime

class Alarm(Base):
    __tablename__ = 'alarm'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, default=datetime.now())
    end_time = Column(DateTime)

    reading_id = Column(Integer, ForeignKey('reading.id'))
    reading = relationship("Reading")

    expectation_id = Column(Integer, ForeignKey('expectation.id'))
    expectation = relationship("Expectation")

    atmospheric_condition_id = Column(Integer, 
                                      ForeignKey('atmospheric_condition.id'))
    
    def __repr__(self):
        return "Alarm(id={!r}, reading={!r}, expectation={!r}, start_time={!r}, end_time={!r})".format(self.id, self.reading, self.expectation, self.start_time, self.end_time)

    def __str__(self):
        return "Alarm: \n\tid: {!r} \n\treading - {}: \n\texpectation - {} \n\tstart time: {!s} \n\tend time: {!s}".format(self.id, str(self.reading).replace("\n", "\n\t"), str(self.expectation).replace("\n", "\n\t"), self.start_time, self.end_time)

    def active(self):
        return self.start_time is not None and self.end_time is None

    def end(self):
        if self.end_time is None:
            self.end_time = datetime.now()
        else:
            raise AlarmInactiveException
