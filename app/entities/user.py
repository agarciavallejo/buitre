from sqlalchemy import Column, String, Numeric, Integer, Boolean
from sqlalchemy.orm import relationship
from .entity import Entity, Base
from marshmallow import Schema, fields


class User(Entity, Base):
    __tablename__ = 'User'

    name = Column("name", String)
    email = Column("email", String)
    password = Column("password", String)
    latitude = Column("latitude", Numeric(9, 6))
    longitude = Column("longitude", Numeric(9, 6))
    radius = Column("radius", Integer)
    is_valid = Column("is_valid", Boolean)
    score = Column("score", Integer)

    tags = relationship("UserTag", back_populates="user")
    opportunities_created = relationship("Opportunity", back_populates="created_by")
    opportunities_liked = relationship("OpportunityLike", back_populates="user")
    comments_created = relationship("Comment", back_populates="created_by")
    comments_liked = relationship("CommentLike", back_populates="user")

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
