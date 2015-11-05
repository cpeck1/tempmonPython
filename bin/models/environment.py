import os, pprint
from datetime import datetime

from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

from bin.models.alarm import Alarm

class Environment(Base):
    """Class representing an environment with conditions to be monitored

    Attributes:
    name: The name given to this environment
    serial: the unique identifier assigned to this environment
    """
    __tablename__ = 'environment'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    serial = Column(String, unique=True)

    quantitative_properties = relationship("QuantitativeProperty",
                                          backref='environment',
                                          cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "Environment(id={}, name={}, serial={}, properties={})".format(
            self.id,
            self.name,
            self.serial,
            [p for p in self.quantitative_properties]
        )

