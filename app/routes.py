from . import app
from flask import  jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Config
from .entities.user import User, UserSchema
from .entities.opportunity import Opportunity, OpportunitySchema
from .entities.entity import Base
from .controller import Controller

# database
app.config.from_object(Config)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

session = Session()
c = Controller(session)


# create test user
initial_users = session.query(User).all()
if len(initial_users) == 0:
    test_user = User("test2", "script")
    test_user.is_valid = True
    session.add(test_user)
    session.commit()
    session.close()

# public methods
@app.route('/')

@app.route("/users")
def get_users():
    users_object = session.query(User).all()
    user_schema = UserSchema(many=True)
    users = user_schema.dump(users_object)
    session.close()
    return jsonify(users)


@app.route("/opportunity")
def list_opportunities():
    db_oppos = session.query(Opportunity).all()
    o_sch = OpportunitySchema(many=True)
    opportunities = o_sch.dump(db_oppos)
    session.close()
    return jsonify(opportunities)


# route params test
@app.route("/opportunity/create/<user_id>")
def create_opo(user_id):
    user = c.getUser(user_id)
    if(user):
        c.createOpportunity("Oportunitat2", user_id)
        return "DONE"
    else:
        return "USER NOT FOUND"

# query string params test
@app.route("/opportunity/find")
def create_opportunity():
    q = request.args
    return jsonify(q)


@app.route("/test")
def test_action():
    opo_id = 1
    user_id = 1
    sch_id = c.createOportunitySchedule(user_id, opo_id, "8:00", "16:30")
    return "Schedule created with id: %s" % sch_id
    db_sch = session.query(OportunitySchedule).all()
    session.close()
    o_sch = OportunityScheduleSchema(many=True)
    schedules = o_sch.dump(db_sch)

    return jsonify(schedules)
