import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '#buitres_4eva-666'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://app:1234@localhost:5432/buitre'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
