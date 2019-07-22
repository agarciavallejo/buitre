from flask import Blueprint, request, jsonify
from ..entities.user import UserRepository, UserFactory
from ..services.user.createUserService import CreateUserService
from ..services.user.loginUserService import LoginUserService
from ..services.user.ValidateUserService import ValidateUserService
from ..libs.exceptions import \
    EmailInUseException, \
    ArgumentException, \
    AuthenticationException, \
    NoValidUserException, \
    UserValidationException
from ..libs.utils import TokenManager
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


@user_api.route('/delete/<int:id>', methods=['GET'])
def get_user(id):
    response = {}
    response_code = 200

    UserRepository.delete(id)
    response['success'] = True

    return jsonify(response), response_code
