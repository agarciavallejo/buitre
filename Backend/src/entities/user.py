from sqlalchemy import Column, String, Numeric, Integer, Boolean
from .entity import Entity, Base

class User(Entity, Base):
    __tablename__ = 'User'
    
    name = Column(String)
    email = Column(String)
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    radius = Column(Integer)
    is_valid = Column(Boolean)
    score = Column(Integer)
