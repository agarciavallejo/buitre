from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from .entity import Entity, Base
from marshmallow import Schema, fields


class Opportunity(Entity, Base):
    __tablename__ = 'Opportunity'

    name = Column("name", String)
    description = Column("description", String)
    latitude = Column("latitude", Numeric(9, 6))
    longitude = Column("longitude", Numeric(9, 6))
    score = Column("score", Numeric)
    closing_date = Column("closing_date", Date)
    user_id = Column("user_id", Integer, ForeignKey('User.id'), nullable=False)
    user = relationship("User", back_populates="opportunities")

    def __init__(self, name, user_id, description="",
        latitude=None, longitude=None, score=0, closing_date=None):
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.score = score
        self.closing_date = closing_date
        self.user_id = user_id


class OpportunitySchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    description = fields.Str()
    latitude = fields.Decimal()
    longitude = fields.Decimal()
    score = fields.Decimal()
    closing_date = fields.Date()
    user_id = fields.Integer()
