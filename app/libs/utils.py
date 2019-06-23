from itsdangerous import TimedSerializer, SignatureExpired, BadTimeSignature
from .exceptions import ExpiredTokenException, InvalidTokenException
from ..routes import app


class TokenManager:

    @staticmethod
    def generate_session_token(payload=None):
        s = TimedSerializer(app.config['SECRET_KEY'])
        return s.dumps(payload)

    @staticmethod
    def verify_session_token(token):
        s = TimedSerializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=app.config['LOGIN_TOKEN_EXPIRATION'])
        except SignatureExpired:
            raise ExpiredTokenException
        except BadTimeSignature:
            raise InvalidTokenException

        return data
