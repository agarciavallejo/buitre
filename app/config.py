import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '#buitres_4eva-666'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://app:1234@localhost:5432/buitre'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_TOKEN_EXPIRATION = 86400  # 1 day
    VALIDATION_TOKEN_EXPIRATION = 604800  # 1 week
    SERVER_NAME = os.environ.get('SERVER_NAME') or 'localhost:5000'
