from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

class Admin(Base):
    """Class for an admin of the system

    Attributes:
    id: the id of this admin assigned by the ORM
    name: the full name of this admin (First Name Middle Names Last Name)
    email_addresses: list of this admin's email addresses
    """
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
        return "Admin(id={!r}, name={!r}, email_addresses={!r})".format(self.id, self.name, self.email)

