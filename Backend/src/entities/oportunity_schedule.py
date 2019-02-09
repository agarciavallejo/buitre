from sqlalchemy import Column, Integer, Time, Boolean, ForeignKey
from .entity import Entity, Base
from marshmallow import Schema, fields


class OportunitySchedule(Entity, Base):
    __tablename__ = 'OportunitySchedule'

    start_time = Column("start_time", Time, nullable=False)
    end_time = Column("end_time", Time, nullable=False)
    monday = Column("monday", Boolean)
    tuesday = Column("tuesday", Boolean)
    wednesday = Column("wednesday", Boolean)
    thursday = Column("thursday", Boolean)
    friday = Column("friday", Boolean)
    saturday = Column("saturday", Boolean)
    sunday = Column("sunday", Boolean)
    oportunity_id = Column("oportunity_id", Integer, ForeignKey('Oportunity.id'),
        nullable=False)

    def __init__(self, opportunity_id, start_time, end_time,
        mo=True, tu=True, we=True, th=True, fr=True, sa=True, su=True):
        self.start_time = start_time
        self.end_time = end_time
        self.monday = mo
        self.tuesday = tu
        self.wednesday = we
        self.thursday = th
        self.friday = fr
        self.saturday = sa
        self.sunday = su
        self.oportunity_id = opportunity_id


class OportunityScheduleSchema(Schema):
    id = fields.Integer()
    oportunity_id = fields.Integer()
    start_time = fields.Time()
    end_time = fields.Time()
    monday = fields.Boolean()
    tuesday = fields.Boolean()
    wednesday = fields.Boolean()
    thursday = fields.Boolean()
    friday = fields.Boolean()
    saturday = fields.Boolean()
    sunday = fields.Boolean()
