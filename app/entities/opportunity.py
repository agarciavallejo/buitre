from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date, or_
from sqlalchemy.orm import relationship

from .opportunityLike import OpportunityLike
from .entity import Entity, Base, session
from marshmallow import Schema, fields


class Opportunity(Entity, Base):
    __tablename__ = 'Opportunity'

    name = Column("name", String)
    description = Column("description", String)
    latitude = Column("latitude", Numeric(9, 6))
    longitude = Column("longitude", Numeric(9, 6))
    score = Column("score", Numeric)
    closing_date = Column("closing_date", Date)
    user_id = Column("user_id", Integer,
                     ForeignKey('User.id'), nullable=False)
    address = Column('address', String)

    comments = relationship("Comment", back_populates="opportunity")
    pictures = relationship("Picture", back_populates="opportunity")
    schedules = relationship("OpportunitySchedule", back_populates="opportunity")
    tags = relationship("OpportunityTag", back_populates="opportunity")
    created_by = relationship("User", back_populates="opportunities_created")
    liked_by = relationship("OpportunityLike", back_populates="opportunity")

    def __init__(self, name, user_id, description="",
                 latitude=None, longitude=None, score=0, closing_date=None, address=None):
        super().__init__(user_id)
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.score = score
        self.closing_date = closing_date
        self.user_id = user_id
        self.address = address

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'score': self.score,
            'closing_date': self.closing_date,
            'user_id': self.user_id,
            'user_name': self.created_by.name,
            'main_picture': [picture.to_dict() for picture in self.pictures][0] if self.pictures else None,
            'pictures': [picture.to_dict() for picture in self.pictures],
            'tags': [oppotag.tag.to_dict() for oppotag in self.tags],
            'comments': [comment.to_dict() for comment in self.comments],
            'schedule': [schedule.to_dict() for schedule in self.schedules],
        }


class OpportunitySchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    description = fields.Str()
    address = fields.Str()
    latitude = fields.Decimal()
    longitude = fields.Decimal()
    score = fields.Decimal()
    closing_date = fields.Date()
    user_id = fields.Integer()


class OpportunityRepository:

    @staticmethod
    def get_by_id(id):
        opportunity = session.query(Opportunity).filter_by(id=id).first()
        return opportunity

    @staticmethod
    def get_by_user_id(user_id):
        opportunities = session.query(Opportunity).filter_by(user_id=user_id).all()
        return opportunities

    @staticmethod
    def get_by_liked_by(user_id):
        liked = []
        oppolikes = session.query(OpportunityLike).filter_by(user_id=user_id).all()
        for like in oppolikes:
            oppo = session.query(Opportunity).get(like.opportunity_id)
            liked.append(oppo)
        return liked

    @staticmethod
    def persist(opportunity):
        return opportunity.persist()

    @staticmethod
    def execute_query(keyword, page_size, page):
        opportunities = session.query(Opportunity) \
            .filter(or_(
                Opportunity.name.like("%" + keyword + "%"),
                Opportunity.description.like("%" + keyword + "%"))) \
            .limit(page_size).offset(page - 1).all()
        return opportunities


class OpportunityFactory:
    @staticmethod
    def create(user_id, name, description, address, latitude, longitude, closing_date):
        oppo = Opportunity(
            name=name,
            user_id=user_id,
            description=description,
            address=address,
            latitude=latitude,
            longitude=longitude,
            closing_date=closing_date,
        )
        return oppo
