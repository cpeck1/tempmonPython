import logging
from bin.models.admin import Admin

logger = logging.getLogger("monitoring_application")

class AdminController:
    def __init__(self, dbsession):
        self.dbsession = dbsession
        self.admins = dbsession.query(Admin).all()

    def report(self, stuff):
        logger.debug(repr(stuff))
