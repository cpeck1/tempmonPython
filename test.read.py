import datetime, time, sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bin.models import base

from bin.controllers.monitoring_controller import MonitoringController

# need to import models in this order so that each is added to the 
# declarative base of sqlalchemy
from bin.models import environment, transmitter, admin
from bin.models import quantitative_property, channel
from bin.models import expectation
from bin.models import reading, alarm

from bin.models.expectation import Expectation
from bin.models.quantitative_property import QuantitativeProperty
from bin.models.environment import Environment

from bin.models.transmitter import Transmitter
from bin.models.channel import Channel
from bin.models.reading import Reading

engine = create_engine("sqlite:////home/connor/workspace/test/test1.db")
base.Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

readings = session.query(Reading).all()
print(readings)
