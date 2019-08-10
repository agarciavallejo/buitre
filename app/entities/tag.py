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
        super().__init__("script")
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

    @staticmethod
    def add_to_user(tag, user_id):
        user_tag = userTag.UserTag(user_id, tag.id)
        user_tag.persist()

    @staticmethod
    def remove_from_user(user_id):
        session.query(userTag.UserTag).filter_by(user_id=user_id).delete()

    @staticmethod
    def get_by_name(name):
        lc_name = str(name).strip().lower()
        return session.query(Tag).filter(Tag.name.ilike(lc_name)).first()

    @staticmethod
    def persist(tag):
        return tag.persist()
