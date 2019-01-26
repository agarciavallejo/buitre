from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config


#create app
app = Flask(__name__)
CORS(app)

#database
app.config.from_object(Config)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

@app.route("/")
def hello():
    return 'hello world'
