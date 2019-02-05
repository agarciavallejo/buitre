from sqlalchemy import Column, String, Numeric, Integer, Boolean
from .entity import Entity, Base
from marshmallow import Schema, fields


class User(Entity, Base):
    __tablename__ = 'User'

    name = Column(String)
    email = Column(String)
    password = Column(String)
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    radius = Column(Integer)
    is_valid = Column(Boolean)
    score = Column(Integer)

    def __init__(self, name, created_by):
        Entity.__init__(self, created_by)
        self.name = name


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()
    latitude = fields.Decimal()
    longitude = fields.Decimal()
    radius = fields.Integer()
    is_valid = fields.Boolean()
    score = fields.Integer()
