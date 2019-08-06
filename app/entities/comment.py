from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .entity import Entity, Base, session
from marshmallow import Schema, fields


class Comment(Entity, Base):
    __tablename__ = 'Comment'

    text = Column("text", String)
    score = Column("score", Numeric)
    opportunity_id = Column("opportunity_id", Integer,
       ForeignKey('Opportunity.id'), nullable=False)
    user_id = Column("user_id", Integer,
        ForeignKey('User.id'), nullable=False)

    opportunity = relationship("Opportunity", back_populates="comments")
    created_by = relationship("User", back_populates="comments_created")
    liked_by = relationship("CommentLike", back_populates="comment")

    def __init__(self, text, user_id, opportunity_id):
        super(Comment, self).__init__(user_id)
        self.text = text
        self.score = 0
        self.opportunity_id = opportunity_id
        self.user_id = user_id


class CommentSchema(Schema):
    id = fields.Integer()
    text = fields.Str()
    score = fields.Decimal()
    opportunity_id = fields.Integer()
    user_id = fields.Integer()


class CommentRepository:
    @staticmethod
    def get_by_user_id(user_id):
        comments = session.query(Comment).filter_by(user_id=user_id).all()
        return comments

