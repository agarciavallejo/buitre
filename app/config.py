import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '#buitres_4eva-666'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')+'?sslmode=require' or \
        'postgresql://app:1234@localhost:5432/buitre'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_TOKEN_EXPIRATION = 86400  # 1 day
    VALIDATION_TOKEN_EXPIRATION = 604800  # 1 week
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'testbuitre@gmail.com',
    MAIL_PASSWORD = 'testbuitre123'

