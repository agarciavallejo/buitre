from sqlalchemy import Column, Integer, ForeignKey
from .entity import Entity, Base
from marshmallow import Schema, fields

class UserTag(Entity, Base):
    __tablename__ = 'UserTag'

    user_id = Column("user_id", Integer, ForeignKey('User.id'), nullable=False, primary_key=True)
    tag_id  = Column("tag_id" , Integer, ForeignKey('Tag.id'),  nullable=False, primary_key=True)

    def __init__(self, user_id, tag_id):
        self.user_id    = user_id
        self.tag_id     = tag_id
        

class UserTagSchema(Schema):
    user_id = fields.Integer()
    tag_id  = fields.Integer()


        