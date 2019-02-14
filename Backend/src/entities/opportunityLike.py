from sqlalchemy import Column, Integer, ForeignKey
from .entity import Entity, Base
from marshmallow import Schema, fields

class OpportunityLike(Entity, Base):
    _tablename__ = 'OportunityLike'
    
    oportunity_id = Column("oportunity_id", Integer, 
        ForeignKey('Oportunity.id'), nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, 
        ForeignKey('User.id'), nullable=False, primary_key=True)
    score = Column(Integer)
    
    def __init__(opportunity_id, user_id, score):
        self.oportunity_id = opportunity_id
        self.user_id = user_id
        self.score = score
        
class OpportunityLikeSchema:
    oportunity_id = fields.Integer()
    user_id = fields.Integer()
    score = fields.Integer()
