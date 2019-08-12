from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .entity import Entity, Base
from marshmallow import Schema, fields


class OpportunityTag(Entity, Base):
    __tablename__ = 'OpportunityTag'

    opportunity_id = Column("opportunity_id", Integer,
                            ForeignKey('Opportunity.id'), nullable=False)
    tag_id = Column("tag_id", Integer,
                    ForeignKey('Tag.id'), nullable=False)

    opportunity = relationship("Opportunity", back_populates="tags")
    tag = relationship("Tag", back_populates="opportunities")

    UniqueConstraint('opportunity_id', 'tag_id')

    def __init__(self, opportunity_id, tag_id):
        super().__init__(None)
        self.opportunity_id = opportunity_id
        self.tag_id = tag_id


class OpportunityTagSchema(Schema):
    opportunity_id = fields.Integer()
    tag_id = fields.Integer()
