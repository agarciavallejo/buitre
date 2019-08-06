import functools
from flask import request, g, jsonify

from ..utils.exceptions import ExpiredTokenException, InvalidTokenException
from ..services.user.authenticateUserService import AuthenticateUserService
from ..services.user.createUserService import CreateUserService
from ..services.user.validateUserService import ValidateUserService
from ..services.user.loginUserService import LoginUserService
from ..services.user.getUserService import GetUserService
from ..services.user.sendUserRecoveryService import SendUserRecoveryService
from ..services.user.recoverUserService import RecoverUserService

from ..utils.tokenManager import TokenManager
from ..utils.email import EmailFactory, EmailSender
from ..entities.user import UserRepository, UserFactory
from werkzeug.security import generate_password_hash, check_password_hash

# INSTANTIATE SERVICES
AuthenticateUserService = AuthenticateUserService(
    token_verifier=TokenManager.verify_session_token
)
CreateUserService = CreateUserService(
    user_repository=UserRepository,
    user_factory=UserFactory,
    password_hasher=generate_password_hash,
    validation_token_generator=TokenManager.generate_validation_token,
    email_factory=EmailFactory,
    email_sender=EmailSender
)
ValidateUserService = ValidateUserService(
    user_repository=UserRepository,
    validation_token_verifier=TokenManager.verify_validation_token
)
LoginUserService = LoginUserService(
    user_repository=UserRepository,
    token_generator=TokenManager.generate_session_token,
    hash_checker=check_password_hash
)
GetUserService = GetUserService(
    user_repository=UserRepository
)
SendUserRecoveryService = SendUserRecoveryService(
    user_repository=UserRepository,
    email_factory=EmailFactory,
    email_sender=EmailSender,
    token_generator=TokenManager.generate_validation_token
)
RecoverUserService = RecoverUserService(
    token_verifier=TokenManager.verify_validation_token,
    user_repository=UserRepository,
    password_hasher=generate_password_hash
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
