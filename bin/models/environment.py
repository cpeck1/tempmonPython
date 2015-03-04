import os, pprint
from datetime import datetime

from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship 

from .alarm import Alarm

class SomeCsvService:
    # for recording readings, this service will likely be the csv library 
    # native to python, although it may require some kind of wrapper
    def read_row():
        pass

    def write_row(csvdir, leadrow, wrow):
        print("Writing header: ", leadrow)
        print("Writing row: ", wrow)
        print("To file: ", csvdir)

class Environment(Base):
    __tablename__ = 'environment'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    serial = Column(String, unique=True)

    atmospheric_conditions = relationship("AtmosphericCondition", 
                                          backref='environment',
                                          cascade="all, delete, delete-orphan")
    # def __init__(self):
    #     self.id = None
    #     self.atmospheric_conditions = []
    #     self.name = ''
        
    #     # full record dir later defined as: 
    #     #     root_dir/atmospheric_condition.category/datetime.date + ".csv"
    #     self.records_root_dir = '.'

    def __repr__(self):
        return "Environment(id={!r}, atmospheric_conditions={}, name={!r})".format(self.id, str(self.atmospheric_conditions).replace('\n', '\t\n'), self.name)

    def __str__(self):
        s = "Environment: \n\t"
        s = s + "id: {!s} \n\t".format(self.id)
        s = s + "name: {!s} \n\t".format(self.name)
        s = s + "atmospheric conditions: \n\t\t"
        for ac in self.atmospheric_conditions:
            s = s + str(ac).replace("\n", "\n\t\t")
            s = s + "\n\t\t"

        return s
