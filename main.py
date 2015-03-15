import time, sys, logging, argparse
from multiprocessing import Process

from datetime import date
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

from bin.services.message_writer import MessageWriter

if __name__ == "__main__": 
    # parse arguments from stdin
    parser = argparse.ArgumentParser(
        description="Placeholder description"
    )

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()

    # load the DB engine using SQLAlchemy
    engine = create_engine("sqlite:////home/connor/workspace/test/test1.db")
    base.Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # set up system loggers
    logger = logging.getLogger("monitoring_application")
    logger.setLevel(logging.DEBUG)
    
    fh = logging.FileHandler("./logs/"+str(date.today())+".log")
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    if args.verbose:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    # initialize the process controllers
    mc = MonitoringController(session)

    # run the processes via python multiprocessing
    monitoring_process = Process(target=mc.run)
    monitoring_process.start()
