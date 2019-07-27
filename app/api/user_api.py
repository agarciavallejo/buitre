from flask import Blueprint, request, jsonify

from ..entities.user import UserRepository, UserFactory
from ..services.user.createUserService import CreateUserService
from ..services.user.loginUserService import LoginUserService
from ..services.user.validateUserService import ValidateUserService
from ..services.user.recoverUserService import RecoverUserService
from ..services.user.sendUserRecoveryService import SendUserRecoveryService
from ..utils.exceptions import \
    EmailInUseException, \
    ArgumentException, \
    AuthenticationException, \
    NoValidUserException, \
    UserValidationException, ExpiredTokenException, InvalidTokenException
from ..utils.tokenManager import TokenManager
from ..utils.email import EmailFactory, EmailSender
from werkzeug.security import generate_password_hash, check_password_hash

user_api = Blueprint('user_api', __name__)


@user_api.route('/create', methods=['POST'])
def create_user():
    response_code = 200
    result = {}
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    args = {
        'name': name,
        'email': email,
        'password': password
    }

    try:
        service = CreateUserService(
            user_repository=UserRepository,
            user_factory=UserFactory,
            password_hasher=generate_password_hash,
            validation_token_generator=TokenManager.generate_validation_token
        )
        service.call(args)
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

    args = {
        'validation_token': validation_token
    }

    service = ValidateUserService(
        user_repository=UserRepository,
        validation_token_verifier=TokenManager.verify_validation_token
    )

    try:
        service.call(args)
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

    args = {
        'email': email,
        'password': password
    }

    try:
        service = LoginUserService(
            user_repository=UserRepository,
            token_generator=TokenManager,
            hash_checker_func=check_password_hash
        )
        token = service.call(args)
        response['token'] = token
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


@user_api.route('/send_recovery', methods=['POST'])
def send_user_recovery():
    response_code = 200
    response = {}
    email = request.form.get('email')

    args = {
        'email': email
    }

    try:
        service = SendUserRecoveryService(
            user_repository=UserRepository,
            email_factory=EmailFactory,
            email_sender=EmailSender,
            token_generator=TokenManager.generate_validation_token
        )
        service.call(args)
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

    args = {
        'recovery_token': recovery_token,
        'password': new_password
    }

    try:
        service = RecoverUserService(
            token_verifier=TokenManager.verify_validation_token,
            user_repository=UserRepository,
            password_hasher=generate_password_hash
        )
        service.call(args)
        response['success'] = True
    except ExpiredTokenException:
        response['error'] = "Expired token"
        response_code = 500
    except InvalidTokenException:
        response['error'] = "Invalid token"
        response_code = 500

    return jsonify(response), response_code


@user_api.route('/delete/<int:id>', methods=['GET'])
def get_user(id):
    response = {}
    response_code = 200

    UserRepository.delete(id)
    response['success'] = True

    return jsonify(response), response_code
