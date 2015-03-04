from ..models.environment import Environment
from .controllers.atmospheric_condition_controller import (
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

        acc = AtmosphericConditionController(conditions)
        return acc
