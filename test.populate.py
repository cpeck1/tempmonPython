import datetime, time, sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bin.models import base

from bin.controllers.monitoring_controller import MonitoringController

# need to import models in this order so that each is added to the 
# declarative base of sqlalchemy
from bin.models import environment, transmitter, admin, address
from bin.models import atmospheric_condition, channel
from bin.models import expectation
from bin.models import reading, alarm

from bin.models.expectation import Expectation
from bin.models.atmospheric_condition import AtmosphericCondition
from bin.models.environment import Environment

from bin.models.channel import Channel
from bin.models.transmitter import Transmitter

engine = create_engine("sqlite:////home/connor/workspace/test/test1.db")
base.Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

exp = [
    Expectation(units="Celsius", low=-90, high=-80),
]

ac = [
    AtmosphericCondition(
        type="Temperature",
        channel_bus = 3,
        channel_address = 7,
        channel_number = 1,
        rec_freq=15,
        expectation=exp[0]
    ),
    AtmosphericCondition(
        type="Temperature",
        channel_bus = 3,
        channel_address = 8,
        channel_number = 1,
        rec_freq=15,
        expectation=exp[0]
    ),
    AtmosphericCondition(
        type="Temperature",
        channel_bus = 1,
        channel_address = 7,
        channel_number = 1,
        rec_freq=15,
        expectation=exp[0]
    )
]

env = [
    Environment(
        name="Chest Freezer",
        serial="6",
        atmospheric_conditions=[ac[0]]
    ),
    Environment(
        name="Chest Freezer",
        serial="5",
        atmospheric_conditions=[ac[1]]
    ),
    Environment(
        name="Chest Freezer",
        serial="12",
        atmospheric_conditions=[ac[2]]
    )
]

for e in env:
    session.add(e)

session.commit()

