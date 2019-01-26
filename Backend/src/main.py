from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from .entities.user import User, UserSchema
from .entities.entity import Base

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
    test_user = User("test", "script")
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
    
