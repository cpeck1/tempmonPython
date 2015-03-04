from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email = Column(String)

    admin_id = Column(Integer, ForeignKey('admin.id'))
