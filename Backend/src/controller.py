from .entities.user import User, UserSchema
from .entities.oportunity import Opportunity, OpportunitySchema


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
        db_opportunity = self.session.query(Opportunity).get(id)
        sch = OpportunitySchema()

    def createOpportunity(self, name, user_id):
        test_opo = Opportunity(name, user_id, description="", latitude=0.0, longitude=0.0, score=0, closing_date=None)
        self.session.add(test_opo)
        self.session.commit()
        return True
