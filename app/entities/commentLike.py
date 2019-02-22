from sqlalchemy import Column, Integer, ForeignKey
from .entity import Entity, Base
from marshmallow import Schema, fields

class OpportunityLike(Entity, Base):
    _tablename__ = 'Comment Like'
    
    comment_id = Column("comment_id", Integer, 
        ForeignKey('Comment.id'), nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, 
        ForeignKey('User.id'), nullable=False, primary_key=True)
    score = Column(Integer)
    
    def __init__(comment_id, user_id, score):
        self.comment_id = comment_id
        self.user_id = user_id
        self.score = score
        
class CommentLikeSchema:
    comment_id = fields.Integer()
    user_id = fields.Integer()
    score = fields.Integer()
