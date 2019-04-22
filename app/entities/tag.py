from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .entity import Entity, Base
from marshmallow import Schema, fields

class Tag(Entity, Base):
    __tablename__ = 'Tag'

    name    = Column("name", String)
    tag_id  = Column("tag_id", Integer, ForeignKey('Tag.id'))

    opportunities = relationship("OpportunityTag", back_populates="tag")

    def __init__(self, name, tag_id=None):
        self.name = name
        if(tag_id != None):
        	self.tag_id = tag_id
        

class TagSchema(Schema):
    id  = fields.Integer()
    name = fields.Str()
    tag_id = fields.Integer()


        