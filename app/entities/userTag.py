from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .entity import Entity, Base
from marshmallow import Schema, fields


class UserTag(Entity, Base):
    __tablename__ = 'UserTag'

    user_id = Column("user_id", Integer, ForeignKey('User.id'),
                     nullable=False)
    tag_id = Column("tag_id", Integer, ForeignKey('Tag.id'),
                    nullable=False)

    user = relationship("User", back_populates="tags")
    tag = relationship("Tag", back_populates="users")

    UniqueConstraint('user_id', 'tag_id')

    def __init__(self, user_id, tag_id):
        super().__init__(user_id)
        self.user_id = user_id
        self.tag_id = tag_id


class UserTagSchema(Schema):
    user_id = fields.Integer()
    tag_id = fields.Integer()
