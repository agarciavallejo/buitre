from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from .exceptions import ExpiredTokenException, InvalidTokenException
from ..routes import app


class TokenManager:

    @staticmethod
    def generate_session_token(payload=None):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return s.dumps(payload)

    @staticmethod
    def verify_session_token(token):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=app.config['LOGIN_TOKEN_EXPIRATION'])
        except SignatureExpired:
            raise ExpiredTokenException
        except BadTimeSignature:
            raise InvalidTokenException

        return data

    @staticmethod
    def generate_validation_token(user_email):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = s.dumps(str(user_email))
        return token

    @staticmethod
    def verify_validation_token(token):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=app.config['VALIDATION_TOKEN_EXPIRATION'])
        except SignatureExpired:
            raise ExpiredTokenException
        except BadTimeSignature:
            raise InvalidTokenException

        return data
