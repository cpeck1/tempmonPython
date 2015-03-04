import datetime, time, sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import base

from controllers.monitoring_controller import MonitoringController

# need to import models in this order so that each is added to the 
# declarative base of sqlalchemy
from models import environment, transmitter, admin
from models import atmospheric_condition, channel
from models import expectation
from models import reading, alarm

from models.expectation import Expectation
from models.atmospheric_condition import AtmosphericCondition
from models.environment import Environment

from models.transmitter import Transmitter
from models.channel import Channel

engine = create_engine("sqlite:////home/connor/workspace/test/test.db")
base.Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()
e = session.query(Environment).all()
for env in e:
    print(env)

t = session.query(Transmitter).all()
for trans in t:
    print(trans)
