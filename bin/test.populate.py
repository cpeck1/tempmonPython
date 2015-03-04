import datetime, time, sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import base

from controllers.monitoring_controller import MonitoringController

# need to import models in this order so that each is added to the 
# declarative base of sqlalchemy
from models import environment, transmitter, admin, address
from models import atmospheric_condition, channel
from models import expectation
from models import reading, alarm

from models.expectation import Expectation
from models.atmospheric_condition import AtmosphericCondition
from models.environment import Environment

from models.channel import Channel
from models.transmitter import Transmitter

engine = create_engine("sqlite:////home/connor/workspace/test/test1.db")
base.Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

exp = [
    Expectation(units="Celsius", low=-90, high=-80),
    Expectation(units="Celsius", low=-40, high=-20),
    Expectation(units="Celsius", low=-10, high=-20),
    Expectation(units="Percent", low=40, high=60)
]

ac = [
    AtmosphericCondition(
        type="Temperature",
        channel_bus = 0,
        channel_address = 0,
        channel_number = 1,
        rec_freq=15,
        expectation=exp[0]
    ),
    AtmosphericCondition(
        type="Temperature",
        channel_bus = 0,
        channel_address = 1,
        channel_number = 1,
        rec_freq=15,
        expectation=exp[0]
    ),
    AtmosphericCondition(
        type="Temperature",
        channel_bus = 0,
        channel_address = 2,
        channel_number = 1,
        rec_freq=15,
        expectation=exp[1]
    ),
    AtmosphericCondition(
        type="Temperature",
        channel_bus = 1,
        channel_address = 0,
        channel_number = 1,
        rec_freq=15,
        expectation=exp[2]
    ),
    AtmosphericCondition(
        type="Relative Humidity",
        channel_bus = 1,
        channel_address = 1,
        channel_number = 1,
        rec_freq=15,
        expectation=exp[3]
    ),
    AtmosphericCondition(
        type="Relative Humidity",
        channel_bus = 1,
        channel_address = 2,
        channel_number = 1,
        rec_freq=15,
        expectation=exp[3]
    )
]

env = [
    Environment(
        name="Chest Freezer",
        atmospheric_conditions=[ac[0], ac[4]]
    ),
    Environment(
        name="Chest Freezer",
        atmospheric_conditions=[ac[1]]
    ),
    Environment(
        name="Chest Freezer",
        atmospheric_conditions=[ac[2], ac[5]]
    ),
    Environment(
        name="Chest Freezer",
        atmospheric_conditions=[ac[3]]
    )
]

for e in env:
    session.add(e)

session.commit()

