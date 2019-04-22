from .entities.user import User, UserSchema
from .entities.opportunity import Opportunity, OpportunitySchema
from .entities.opportunitySchedule import OpportunitySchedule, OpportunityScheduleSchema
from .entities.picture import Picture
from .entities.tag import Tag


class Controller:

    session = None

    def __init__(self, session):
        self.session = session

    def getUser(self, user_id):
        sch = UserSchema()
        db_user = self.session.query(User).get(user_id)
        if (None == db_user):
            return None  # raise UserNotFoundException
        return sch.dump(db_user)

    def getOpportunity(self, id):
        sch = OpportunitySchema()
        db_opportunity = self.session.query(Opportunity).get(id)
        if(None == db_opportunity):
            return None
        return sch.dump(db_opportunity)

    def createOpportunity(self, name, user_id):
        test_opo = Opportunity(
            name,
            user_id,
            description="",
            latitude=0.0,
            longitude=0.0,
            score=0,
            closing_date=None)
        self.session.add(test_opo)
        self.session.commit()
        return test_opo.id

    def opportunityAddTag(self, opportunity_id, tag_id):
        opp_tag = OppotunityTag(opportunity_id, tag_id)
        self.session.add(opp_tag)
        self.session.flush()
        self.session.commit()

    def createOpportunitySchedule(self, user_id, opportunity_id, stime, etime,
        mo=True, tu=True, we=True, th=True, fr=True, sa=True, su=True):

        test_schedule = OpportunitySchedule(
            user_id,
            opportunity_id,
            stime,
            etime,
            mo, tu, we, th, fr, sa, su
        )
        self.session.add(test_schedule)
        self.session.flush()
        self.session.commit()
        return test_schedule.id

    def createOpportunityPicture(self, opportunity_id, path):
        picture = Picture(
            opportunity_id,
            path
        )

        self.session.add(picture)
        self.session.flush()
        self.session.commit()
        return picture.id

    def createTag(self, name):
        tag = Tag(name)
        self.session.add(tag)
        self.session.flush()
        self.session.commit()
        return tag.id
