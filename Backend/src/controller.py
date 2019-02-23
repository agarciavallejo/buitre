from entities.user import User, UserSchema
from entities.oportunity import Oportunity, OportunitySchema
from entities.oportunity_schedule import OportunitySchedule, OportunityScheduleSchema


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

    def getOportunity(self, id):
        db_oportunity = self.session.query(Oportunity).get(id)
        sch = OportunitySchema()

    def createOportunity(self, name, user_id):
        test_opo = Oportunity(
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

    def createOportunitySchedule(self, user_id, oportunity_id, stime, etime,
        mo=True, tu=True, we=True, th=True, fr=True, sa=True, su=True):

        test_schedule = OportunitySchedule(
            user_id,
            oportunity_id,
            stime,
            etime,
            mo, tu, we, th, fr, sa, su
        )
        self.session.add(test_schedule)
        self.session.flush()
        self.session.commit()
        return test_schedule.id
