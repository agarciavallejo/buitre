from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Backend.config import Config
from .entities.user import User, UserSchema
from .entities.oportunity import Oportunity, OportunitySchema
from .entities.entity import Base
from controller import Controller

# Comment added to test autopep hook

#create app
app = Flask(__name__)
CORS(app)

#database
app.config.from_object(Config)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
             
session = Session()

#create test user
initial_users = session.query(User).all()
if len(initial_users) == 0:
    test_user = User("test2", "script")
    test_user.is_valid = True;
    session.add(test_user)
    session.commit()
    session.close()

#public methods
@app.route("/users")
def get_users():
    users_object = session.query(User).all()
    user_schema = UserSchema(many = True)
    users = user_schema.dump(users_object)
    session.close()
    return jsonify(users)

@app.route("/oportunity")
def list_oportunities():
    db_opos = session.query(Oportunity).all()
    o_sch = OportunitySchema(many = True)
    oportunities = o_sch.dump(db_opos)
    session.close()
    return jsonify(oportunities)


# route params test
@app.route("/oportunity/create/<user_id>")
def create_opo(user_id):
    c = Controller(session)
    user = c.getUser(user_id)
    if(user):
        c.createOportunity("Oportunitat2",user_id)
        return "DONE"
    else:
        return "USER NOT FOUND"

# query string params test
@app.route("/oportunity/find")
def create_oportunity():
    q = request.args
    return jsonify(q)