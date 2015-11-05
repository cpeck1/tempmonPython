import time, signal, sys
from multiprocessing import Process

import logging
logger = logging.getLogger("monitoring_application")

from bin.controllers.environment_controller import EnvironmentController
from bin.models.environment import Environment
from bin.infrastructure.networking_library import NetworkingManager

class _EnvironmentApplication:
    def __init__(self, controller, process, pair):
        self.controller = controller
        self.process = process
        self.pair = pair

class EnvironmentApplicationController:
    def __init__(self, dbsession):
        signal.signal(signal.SIGTERM, self.stop)

        self.dbsession = dbsession
        self.environments = dbsession.query(Environment).all()

        self.environment_applications = []

        self.poller = None

    def stop(self, _signo, _stack_frame):
        self.dbsession.commit()
        logger.info("Environment Application Controller stopping")

        sys.exit(0)

    def create_environment(self, environment):
        child_num = len(self.environment_applications)

        controller = EnvironmentController(
            child_num,
            self.dbsession,
            environment
        )

        process = Process(target=controller.run)
        pair = NetworkingManager.EACParentChildNPairParent(child_num)

        self.poller.register(pair, NetworkingManager.POLLIN)

        environment_application = _EnvironmentApplication(
            controller,
            process,
            pair
        )
        self.environment_applications.append(environment_application)

        environment_application.process.daemon = False
        environment_application.process.start()

    def terminate_subprocesses(self):
        for app in self.environment_applications:
            logger.info(
                "Waiting for app with "+
                repr(app.controller.environment)+
                " to terminate..."
            )
            app.process.join(2)
            if app.process.is_alive():
                logger.warning(
                    "App with "+ repr(app.controller.environment)+
                    " did not terminate safely. "+
                    "Forcing termination..."
                )
                app.process.terminate()

    def run(self):
        logger.info("Environment Application Controller starting")
        subscriber = NetworkingManager.KillBroadcastSubscriber()

        self.poller = NetworkingManager.Poller()
        self.poller.register(subscriber, NetworkingManager.POLLIN)

        for environment in self.environments:
             self.create_environment(environment)

        while True:
            socks = dict(self.poller.poll())

            if subscriber.contained_in(socks):
                message = subscriber.recv_string()
                filter, command = message.split()

                if command == "KILL":
                    self.terminate_subprocesses()
                    logger.info("Environment application controller stopping")
                    break
