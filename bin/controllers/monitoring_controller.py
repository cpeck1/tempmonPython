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
        logger.debug("Monitoring Controller initializing")
        self.dbsession = dbsession

        self.environment_controller = None
        self.transmitter_controller = None
        self.admin_controller = None

        self.condition_controller = None
        logger.debug("Monitoring Controller initialized")

    def run(self):
        logger.warning("Monitoring Controller started")

        load_environment_flag = load_transmitter_flag = load_admin_flag = 1
        while True:
            if load_environment_flag:
                logger.info("Environment Controller initializing")
                self.environment_controller = (
                    EnvironmentController(self.dbsession)
                )
                logger.info("Environment Controller initialized")

                logger.info("Atmospheric Condition Controller initializing")
                self.condition_controller = (
                    self.environment_controller.create_condition_controller()
                ) 
                logger.info("Atmospheric Condition Controller initialized")

            if load_transmitter_flag:
                logger.info("Transmitter Controller initializing")
                self.transmitter_controller = (
                    TransmitterController()
                )
                logger.info("Transmitter Controller initialized")

            if load_admin_flag:
                logger.info("Admin Controller initializing")
                self.admin_controller = (
                    AdminController(self.dbsession)
                )
                logger.info("Admin Controller initialized")
                load_admin_flag = 0

            if load_environment_flag or load_transmitter_flag: 
                logger.info("Transmitter channels opening")
                channels = self.transmitter_controller.open_all_channels()
                logger.info("Transmitter channels opened")

                logger.info("Assigning transmitter channels")
                errors = (
                    self.condition_controller.assign_channels(channels)
                )
                logger.info("Transmitter channels assigned")
                logger.info("Errors: " + str(errors))

                self.admin_controller.report(errors)

                load_environment_flag = load_transmitter_flag = 0
                logger.info("Load block complete")
                
            logger.debug("Gathering readings from channels")
            alarms = self.condition_controller.gather_readings()
            logger.debug("Alarms: " + str(alarms))

            self.admin_controller.report(alarms)
##
