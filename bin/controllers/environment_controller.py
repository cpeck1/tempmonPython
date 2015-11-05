import time, signal, sys
from multiprocessing import Process

from bin.controllers.quantitative_property_controller import (
    QuantitativePropertyController
)
from bin.models.quantitative_property import QuantitativeProperty
from bin.infrastructure.networking_library import NetworkingManager

import logging
logger = logging.getLogger("monitoring_application")

class _QuantitativePropertyApplication:
    def __init__(self, controller, process):
        self.controller = controller
        self.process = process

class EnvironmentController:
    def __init__(self, child_num, dbsession, environment):
        self.running = True

        self.child_num = child_num
        self.environment = environment
        self.dbsession = dbsession

        self.quantitative_property_applications = []

    def stop(self, _signo, _stack_frame):
        for app in self.quantitative_property_applications:
            app.process.terminate()

        self.dbsession.commit()

        logger.warning(
            "Environment controller with "+
            repr(self.environment)+
            " forced to quit. Child processes did not exit safely."
        )
        sys.exit(0)

    def create_quantitative_property(self, p):
        controller = QuantitativePropertyController(self.dbsession, p)
        process = Process(target=controller.run)
        process.daemon = True

        qpa = _QuantitativePropertyApplication(
            controller,
            process
        )

        qpa.process.start()
        self.quantitative_property_applications.append(qpa)

    def terminate_subprocesses(self):
        for app in self.quantitative_property_applications:
            logger.info(
                "Waiting for app with "+
                repr(app.controller.quantitative_property)+
                " to terminate..."
            )
            app.process.join(2)
            if app.process.is_alive():
                logger.warning(
                    "App with "+
                    repr(app.controller.quantitative_property)+
                    " did not terminate safely. "+
                    "Forcing termination..."
                )
                app.process.terminate()


    def run(self):
        logger.info(
            "Environment controller starting with "+
            repr(self.environment)
        )

        for p in self.environment.quantitative_properties:
             self.create_quantitative_property(p)

        subscriber = NetworkingManager.KillBroadcastSubscriber()

        poller = NetworkingManager.Poller()
        poller.register(subscriber, NetworkingManager.POLLIN)

        while True:
            socks = dict(poller.poll())

            if subscriber.contained_in(socks):
                message = subscriber.recv_string()
                filter, command = message.split()

                if command == "KILL":
                    self.terminate_subprocesses()
                    logger.info("Environment controller stopping")
                    break
