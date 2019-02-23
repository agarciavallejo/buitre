from sqlalchemy import Column, Integer, ForeignKey
from .entity import Entity, Base
from marshmallow import Schema, fields


class OpportunityTag(Entity, Base):
    __tablename__ = 'OpportunityTag'

    opportunity_id = Column("opportunity_id", Integer,
        ForeignKey('Opportunity.id'), nullable=False, primary_key=True)
    tag_id = Column("tag_id", Integer,
        ForeignKey('Tag.id'), nullable=False, primary_key=True)

    def __init__(self, opportunity_id, tag_id):
        self.opportunity_id = opportunity_id
        self.tag_id = tag_id


class OpportunityTagSchema(Schema):
    opportunity_id = fields.Integer()
    tag_id = fields.Integer()
