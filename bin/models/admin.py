from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email_addresses = relationship("Address",
                                   backref='admin',
                                   cascade="all, delete, delete-orphan")

    # def __init__(self, id):
    #     self.id = id
    #     self.name = None
    #     self.email = None

    def __repr__(self):
        return "Admin(id={!r}, name={!r}, email={!r})".format(self.id, self.name, self.email)

    def __str__(self):
        return "Admin: \n\tid: {!r} \n\tname: {!r} \n\temail: {!r}".format(self.id or 0, self.name or "None", self.email or "None")
