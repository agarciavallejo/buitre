from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .entity import Entity, Base
from marshmallow import Schema, fields


class Comment(Entity, Base):
    __tablename__ = 'Comment'

    text = Column("text", String)
    score = Column("score", Numeric)
    opportunity_id = Column("opportunity_id", Integer, ForeignKey('Opportunity.id'), nullable=False)
    user_id = Column("user_id", Integer, ForeignKey('User.id'), nullable=False)

    opportunity = relationship("Opportunity")
    user = relationship("User")

    def __init__(self, text, user_id, opportunity_id):
        self.text = text
        self.score = score
        self.opportunity_id = opportunity_id
        self.user_id = user_id


class CommentSchema(Schema):
    id = fields.Integer()
    text = fields.Str()
    score = fields.Decimal()
    opportunity_id = fields.Integer()
    user_id = fields.Integer()
