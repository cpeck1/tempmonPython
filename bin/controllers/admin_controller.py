from models.admin import Admin

class AdminController:
    def __init__(self, dbsession):
        self.dbsession = dbsession
        self.admins = dbsession.query(Admin).all()

    def report(self, stuff):
        pass
