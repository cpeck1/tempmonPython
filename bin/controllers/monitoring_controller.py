import copy, time, logging
from datetime import datetime, timedelta

logger = logging.getLogger("monitoring_application")

from bin.controllers.environment_controller import EnvironmentController
from bin.controllers.transmitter_controller import TransmitterController
from bin.controllers.admin_controller import AdminController
from bin.controllers.atmospheric_condition_controller import (
    AtmosphericConditionController
)

class MonitoringController:
    def __init__(self, dbsession):
        self.dbsession = dbsession

        self.environment_controller = None
        self.transmitter_controller = None
        self.admin_controller = None

        self.condition_controller = None

    def run(self):
        logger.warning("Monitoring Controller started")

        load_environment_flag = load_transmitter_flag = load_admin_flag = 1
        while True:
            if load_environment_flag:
                self.environment_controller = (
                    EnvironmentController(self.dbsession)
                )

                self.condition_controller = (
                    self.environment_controller.create_condition_controller()
                ) 

            if load_transmitter_flag:
                self.transmitter_controller = (
                    TransmitterController()
                )

            if load_admin_flag:
                self.admin_controller = (
                    AdminController(self.dbsession)
                )
                load_admin_flag = 0

            if load_environment_flag or load_transmitter_flag: 
                channels = self.transmitter_controller.open_all_channels()

                logger.info("Assigning transmitter channels")
                errors = (
                    self.condition_controller.assign_channels(channels)
                )
                logger.info("Transmitter channels assigned")
                logger.info("Errors: " + str(errors))

                self.admin_controller.report(errors)

                load_environment_flag = load_transmitter_flag = 0
                
            logger.debug("Gathering readings from channels")
            alarms = self.condition_controller.gather_readings()
            logger.debug("Alarms: " + str(alarms))

            self.admin_controller.report(alarms)
##
