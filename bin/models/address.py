from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

class Address(Base):
    """Simple email address class

    Attributes:
    id: the id of this address assigned by the ORM
    email: the address of interest
    admin_id: the id of the admin to whom this email belongs
    """
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email = Column(String)

    admin_id = Column(Integer, ForeignKey('admin.id'))

    def __repr__(self):
        return "Address(id={}, email={}, admin_id={})".format(
            self.id, self.email, self.admin_id
        )
