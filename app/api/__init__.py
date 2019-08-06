import functools
from flask import request, g, jsonify

from ..utils.exceptions import ExpiredTokenException, InvalidTokenException
from ..services.user.authenticateUserService import AuthenticateUserService
from ..utils.tokenManager import TokenManager

AuthenticateUserService = AuthenticateUserService(
    token_verifier=TokenManager.verify_session_token
)


def authenticate_user(f):
    @functools.wraps(f)
    def authentication_decorator(*args, **kwargs):
        response = {}
        token = request.args.get('auth_token')
        if token is None:
            response['message'] = 'missing auth_token GET param'
            response_code = 401
            return jsonify(response), response_code

        try:
            user_id = AuthenticateUserService.call({
                'token': token
            })
            g.user_id = user_id
        except (ExpiredTokenException, InvalidTokenException) as e:
            response['message'] = e.message
            response_code = 401
            return jsonify(response), response_code
        return f(*args, **kwargs)

    return authentication_decorator
