import logging
logger = logging.getLogger("monitoring_application")

from bin.models.environment import Environment
from bin.controllers.atmospheric_condition_controller import (
    AtmosphericConditionController
)
class EnvironmentController:
    def __init__(self, dbsession):
        self.dbsession = dbsession
        self.environments = dbsession.query(Environment).all()

    def create_condition_controller(self):
        # avoiding "incomprehensible list comprehension"
        conditions = []
        for e in self.environments:
            for ac in e.atmospheric_conditions:
                conditions.append(ac)
                logger.info(
                    "Creating condition controller with conditions: " + (
                        repr(conditions)
                    )
                )
        acc = AtmosphericConditionController(self.dbsession, conditions)
        return acc
