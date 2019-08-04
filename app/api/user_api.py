from flask import Blueprint, request, jsonify

from datetime import datetime, timedelta

from ..routes import app
from ..entities.user import UserRepository, UserFactory
from ..services.user.createUserService import CreateUserService
from ..services.user.loginUserService import LoginUserService
from ..services.user.validateUserService import ValidateUserService
from ..services.user.authenticateUserService import AuthenticateUserService
from ..services.user.getUserService import GetUserService
from ..services.user.sendUserRecoveryService import SendUserRecoveryService
from ..services.user.recoverUserService import RecoverUserService
from ..utils.exceptions import \
    EmailInUseException, \
    ArgumentException, \
    AuthenticationException, \
    NoValidUserException, \
    UserValidationException, ExpiredTokenException, InvalidTokenException, UserNotFoundException
from ..utils.tokenManager import TokenManager
from ..utils.email import EmailFactory, EmailSender
from werkzeug.security import generate_password_hash, check_password_hash

user_api = Blueprint('user_api', __name__)

# Instantiate services
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
AuthenticateUserService = AuthenticateUserService(
    token_verifier=TokenManager.verify_session_token
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


@user_api.route('/create', methods=['POST'])
def create_user():
    response_code = 200
    result = {}
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        CreateUserService.call({
            'name': name,
            'email': email,
            'password': password
        })
        result['success'] = True
    except (EmailInUseException, ArgumentException) as e:
        result['error'] = e.message
        response_code = 500

    return jsonify(result), response_code


@user_api.route('/validate', methods=['GET'])
def validate_user():
    response_code = 200
    response = {}
    validation_token = request.args.get('validation_token')

    try:
        ValidateUserService.call({
            'validation_token': validation_token
        })
        response['success'] = True
    except UserValidationException as e:
        response['error'] = e.message
        response_code = 500

    return jsonify(response), response_code


@user_api.route('/login', methods=['POST'])
def login_user():
    response_code = 200
    response = {}
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        token = LoginUserService.call({
            'email': email,
            'password': password
        })
        response['token'] = token
        now = datetime.now()
        expiration = now + timedelta(seconds=app.config.get('LOGIN_TOKEN_EXPIRATION'))
        response['expiration'] = expiration.isoformat()
    except ArgumentException as e:
        response['error'] = e.message
        response_code = 500
    except AuthenticationException as e:
        response['error'] = e.message
        response_code = 401
    except NoValidUserException as e:
        response['error'] = e.message
    except Exception as e:
        raise e

    return jsonify(response), response_code


@user_api.route('/get', methods=['GET'])
def get_user():
    response = {}
    response_code = 200

    token = request.args.get('auth_token')
    if token is None:
        response['message'] = 'missing auth_token GET param'
        response_code = 401
        return jsonify(response), response_code

    try:
        user_id = AuthenticateUserService.call({
            'token': token
        })
    except (ExpiredTokenException, InvalidTokenException) as e:
        response['message'] = e.message
        response_code = 401
        return jsonify(response), response_code

    try:
        response = GetUserService.call({
            'user_id': user_id
        })
    except UserNotFoundException as e:
        response['message'] = e.message

        response_code = 500

    return jsonify(response), response_code


@user_api.route('/send_recovery', methods=['POST'])
def send_user_recovery():
    response = {}
    response_code = 200
    email = request.form.get('email')

    try:
        SendUserRecoveryService.call({
            'email': email
        })
    except ArgumentException as e:
        response_code = 500
        response['error'] = e.message
    except AuthenticationException as e:
        response_code = 500
        response['error'] = "User does not exist"

    return jsonify(response), response_code


@user_api.route('/recover', methods=['GET'])
def recover_user():
    response_code = 200
    response = {}

    recovery_token = request.args.get('recovery_token')
    new_password = request.args.get('password')

    try:
        RecoverUserService.call({
            'recovery_token': recovery_token,
            'password': new_password
        })
        response['success'] = True
    except ExpiredTokenException:
        response['error'] = "Expired token"
        response_code = 500
    except InvalidTokenException:
        response['error'] = "Invalid token"
        response_code = 500

    return jsonify(response), response_code


@user_api.route('/delete/<int:id>', methods=['GET'])
def delete_user(id):
    response = {}
    response_code = 200

    UserRepository.delete(id)
    response['success'] = True

    return jsonify(response), response_code
