from sqlalchemy import Column, Time, Boolean, ForeignKey
from .entity import Entity, Base
from marshmallow import Schema, fields


class OpportunitySchedule(Entity, Base):
    _tablename__ = 'OportunitySchedule'

    oportunity_id = Column("oportunity_id", Integer,
        ForeignKey('Oportunity.id'), nullable=False, primary_key=True)
    start_time = Column("start_time", Time)
    end_time = Column("end_time", Time)
    monday = Column("monday", Boolean)
    tuesday = Column("tuesday", Boolean)
    wednesday = Column("wednesday", Boolean)
    thursday = Column("thursday", Boolean)
    friday = Column("friday", Boolean)
    saturday = Column("saturday", Boolean)
    sunday = Column("sunday", Boolean)

    def __init__(opportunity_id, start_time, end_time,
        mo, tu, we, th, fr, sa, su):
        self.oportunity_id = opportunity_id
        self.start_time = start_time
        self.end_time = end_time
        self.monday = mo
        self.tuesday = tu
        self.wednesday = we
        self.thursday = th
        self.friday = fr
        self.saturday = sa
        self.sunday = su


class OpportunityLikeSchema:
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
