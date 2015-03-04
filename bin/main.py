import time, sys

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

from services.message_writer import MessageWriter

if __name__ == "__main__":
    engine = create_engine("sqlite:////home/connor/workspace/test/test1.db")
    base.Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    mc = MonitoringController(session)
    mc.run()
