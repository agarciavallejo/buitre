from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import userTag
from .entity import Entity, Base, session
from marshmallow import Schema, fields


class Tag(Entity, Base):
    __tablename__ = 'Tag'

    name = Column("name", String)
    tag_id = Column("tag_id", Integer, ForeignKey('Tag.id'))

    opportunities = relationship("OpportunityTag", back_populates="tag")
    users = relationship("UserTag", back_populates="tag")

    def __init__(self, name, tag_id=None):
        self.name = name
        self.tag_id = tag_id


class TagSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    tag_id = fields.Integer()


class TagRepository:

    @staticmethod
    def get_by_user_id(user_id):
        tags = []
        user_tags = session.query(userTag.UserTag).filter_by(user_id=user_id).all()
        for user_tag in user_tags:
            tag = session.query(Tag).get(user_tag.tag_id)
            tags.append(tag)

        return tags
