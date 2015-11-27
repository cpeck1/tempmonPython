import time, sys, logging, argparse, zmq
from multiprocessing import Process

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bin.models import base
from bin.controllers.usb_port_controller import UsbPortController
from bin.controllers.transmitter_application_controller import (
    TransmitterApplicationController
)
# from bin.controllers.environment_application_controller import (
#     EnvironmentApplicationController
# )

# need to import models in this order so that each is added to the
# declarative base of sqlalchemy
from bin.models import environment, transmitter, admin, address
from bin.models import quantitative_property, channel
from bin.models import expectation
from bin.models import reading, alarm

from bin.models.command import Command
from bin.services.networking.message import (CommandMessage, DocumentMessage)
from bin.services.networking.networking_manager import NetworkingManager

if __name__ == "__main__":
    # parse arguments from stdin
    parser = argparse.ArgumentParser(
        description="Placeholder description"
    )

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()

    # load the DB engine using SQLAlchemy
    engine = create_engine("sqlite:////home/connor/workspace/test1.db")
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

    # initialize messaging
    kbpublisher = NetworkingManager.KillBroadcastPublisher()

    # initialize the process controllers
    usb_port_controller = UsbPortController()
    upc = Process(target=usb_port_controller.run)
    upc.daemon = True
    upc.start()

    transmitter_application_controller = TransmitterApplicationController()
    tap = Process(target=transmitter_application_controller.run)
    tap.daemon = False
    tap.start()

    # environment_application_controller = EnvironmentApplicationController(
    #     session
    # )
    # ec = Process(target=environment_application_controller.run)
    # ec.daemon = False
    # ec.start()

    # time.sleep(10)
    # logger.info("Attempting to terminate transmitter application controller..")
    # tap.terminate()

    # upc.join()
    # tap.join()
    try:
        input()
    except EOFError:
        attempts = 0
        command = Command.SHUTDOWN
        message = CommandMessage(command=command.value).serialize()
        while tap.is_alive() or upc.is_alive():
            kbpublisher.send_string(message)
