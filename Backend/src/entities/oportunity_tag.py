from sqlalchemy import Column, Integer, ForeignKey
from .entity import Entity, Base
from marshmallow import Schema, fields

class OportunityTag(Entity, Base):
    __tablename__ = 'OportunityTag'

    oportunity_id   = Column("oportunity_id", Integer, 
        ForeignKey('Oportunity.id'), nullable=False, primary_key=True)
    tag_id          = Column("tag_id"       , Integer, 
        ForeignKey('Tag.id'),        nullable=False, primary_key=True)

    def __init__(self, oportunity_id, tag_id):
        self.oportunity_id  = oportunity_id
        self.tag_id         = tag_id
        

class OportunityTagSchema(Schema):
    oportunity_id   = fields.Integer()
    tag_id          = fields.Integer()


        