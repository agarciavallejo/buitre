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
    session_token = Column('session_token', String)
    validation_token = Column('validation_token', String)

    tags = relationship("UserTag", back_populates="user")
    opportunities_created = relationship("Opportunity", back_populates="created_by")
    opportunities_liked = relationship("OpportunityLike", back_populates="user")
    comments_created = relationship("Comment", back_populates="created_by")
    comments_liked = relationship("CommentLike", back_populates="user")

    def __init__(self, name, email, password, created_by=None):
        super(User, self).__init__(created_by)
        self.name = name
        self.email = email
        self.password = password

    def has_been_validated(self):
        return self.is_valid


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
    session_token = fields.Str()
    validation_token = fields.Str()


class UserRepository:

    @staticmethod
    def get_by_email(email):
        user = session.query(User).filter_by(email=email).first()
        return user

    @staticmethod
    def get_by_id(id):
        user = session.query(User).filter_by(id=id).first()
        return user

    @staticmethod
    def validate(id):
        user = UserRepository.get_by_id(id)
        user.is_valid = True
        UserRepository.persist(user)
        return user

    @staticmethod
    def persist(user):
        user.persist()

    @staticmethod
    def delete(id):
        user = UserRepository.get_by_id(id)
        session.delete(user)
        session.commit()
        return True


class UserFactory:

    @staticmethod
    def create(name, email, password, created_by=None):
        user = User(name, email, password, created_by)
        user.is_valid = False
        return user
