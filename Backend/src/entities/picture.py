from sqlalchemy import Column, Integer, ForeignKey, String
from .entity import Entity, Base
from marshmallow import Schema, fields

class Picture(Entity, Base):
    __tablename__ = 'Picture'
    
    oportunity_id = Column("oportunity_id", Integer, 
        ForeignKey('Oportunity.id'), nullable=False)
    path = Column(String)
    
    def __init__(self, opportunity_id, path):
        self.oportunity_id = opportunity_id
        self.path = path
        
class PictureSchema:
    id = fields.Integer()
    oportunity_id = fields.Integer()
    path = fields.Str()
