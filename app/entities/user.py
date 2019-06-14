from sqlalchemy import Column, String, Numeric, Integer, Boolean
from sqlalchemy.orm import relationship
from .commentLike import CommentLike
from .entity import Entity, Base, session
from .opportunityLike import OpportunityLike
from .userTag import UserTag
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

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def persist(self):
        session.add(self)
        session.commit()
        session.close()

    @staticmethod
    def getByEmail(email):
        user = session.query(User).filter_by(email = email).one_or_none()
        return user


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
