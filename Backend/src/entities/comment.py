from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date
from .entity import Entity, Base
from marshmallow import Schema, fields

class Comment(Entity, Base):
    __tablename__ = 'Comment'

    text            = Column("text", String)
    description     = Column("description", String)
    score           = Column("score", Numeric)
    oportunity_id 	= Column("oportunity_id", Integer, ForeignKey('Oportunity.id'), nullable=False)
    user_id         = Column("user_id", Integer, ForeignKey('User.id'), nullable=False)

    def __init__(self, text, user_id, oportunity_id, text):
        self.text = text
        self.score = score
        self.oportunity_id = oportunity_id
        self.user_id = user_id
        

class CommentSchema(Schema):
    id  = fields.Integer()
    text = fields.Str()
    score = fields.Decimal()
    oportunity_id = fields.Integer()
    user_id = fields.Integer()


        