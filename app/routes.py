from . import app
from flask import  jsonify, request
from .entities.user import User, UserSchema
from .entities.opportunity import Opportunity, OpportunitySchema
from .entities.entity import Base, session
from .controller import Controller
from .utils import BuitreEncoder
from .ql import qlschema, GraphQLView
from .api.user_api import user_api

app.debug = True

c = Controller(session)

app.json_encoder = BuitreEncoder
app.register_blueprint(user_api, url_prefix='/api/user')

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

@app.route("/opportunity/<id>/picture/add")
def create_opportunity_picture(id):
    opportunity = c.getOpportunity(id)
    if(opportunity):
        path = "path/to/a/file.png"
        c.createOpportunityPicture(id, path)
        return "DONE"
    else:
        return "NOT DONE"

# query string params test
@app.route("/opportunity/find")
def create_opportunity():
    q = request.args
    return jsonify(q)

@app.route('/opportunity/<id>/addtag/<tag_id>')
def add_tag_to_opportunity(id,tag_id):
    c.opportunityAddTag(int(id), int(tag_id))

@app.route('/tag')
def list_tags():
    return jsonify(c.getTags())

@app.route("/tag/create/<name>")
def create_tag(name):
    id = c.createTag(name)
    return "Tag %s created with id %s" % (name, id)

@app.route("/test")
def test_action():
    opo_id = 1
    user_id = 1
    sch_id = c.createOpportunitySchedule(user_id, opo_id, "8:00", "16:30")
    return "Schedule created with id: %s" % sch_id
    db_sch = session.query(OpportunitySchedule).all()
    session.close()
    o_sch = OpportunityScheduleSchema(many=True)
    schedules = o_sch.dump(db_sch)

    return jsonify(schedules)
    
# GraphQL Interface

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=qlschema,
        graphiql=True # for having the GraphiQL interface
    )
)
