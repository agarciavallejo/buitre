from sqlalchemy import Column, Integer, ForeignKey
from .entity import Entity, Base
from marshmallow import Schema, fields


class OpportunityLike(Entity, Base):
    __tablename__ = 'OpportunityLike'

    opportunity_id = Column("opportunity_id", Integer,
        ForeignKey('Opportunity.id'), nullable=False, primary_key=True)
    user_id = Column("user_id", Integer,
        ForeignKey('User.id'), nullable=False, primary_key=True)
    score = Column(Integer)

    opportunity = relationship("Opportunity", back_populates="liked_by")
    user = relationship("User", back_populates="opportunities_liked")

    def __init__(opportunity_id, user_id, score):
        self.opportunity_id = opportunity_id
        self.user_id = user_id
        self.score = score


class OpportunityLikeSchema:
    opportunity_id = fields.Integer()
    user_id = fields.Integer()
    score = fields.Integer()
