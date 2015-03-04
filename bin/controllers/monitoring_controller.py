import copy, time
from datetime import datetime, timedelta

from controllers.environment_controller import EnvironmentController
from controllers.transmitter_controller import TransmitterController
from controllers.admin_controller import AdminController
from controllers.atmospheric_condition_controller import (
    AtmosphericConditionController
)

class MonitoringController:
    def __init__(self, dbsession):
        self.dbsession = dbsession

        self.environment_controller = EnvironmentController(self.dbsession)
        self.transmitter_controller = TransmitterController(self.dbsession)
        self.admin_controller = AdminController(self.dbsession)

        self.condition_controller = (
            self.environment_controller.create_condition_controller()
        )

    def run(self):
        load_environment_flag = load_transmitter_flag = load_admin_flag = 0

        channels = self.transmitter_controller.open_all_channels()
        errors = (
            self.condition_controller.assign_channels(channels)
        )
        self.admin_controller.report(errors)
        
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
                    TransmitterController(self.dbsession)
                )
            if load_admin_flag:
                self.admin_controller = (
                    AdminController(self.dbsession)
                )
                load_admin_flag = 0
            if load_environment_flag or load_transmitter_flag: 
                channels = self.transmitter_controller.open_all_channels()
                errors = (
                    self.condition_controller.assign_channels(channels)
                )
                self.admin_controller.report(errors)
                load_environment_flag = load_transmitter_flag = 0
                
            alarms = self.condition_controller.gather_readings()
            self.admin_controller.report(alarms)
