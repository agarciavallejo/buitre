from flask import Blueprint, request, jsonify, g

from datetime import datetime, timedelta

from ..api import authenticate_user, CreateUserService, ValidateUserService, LoginUserService, GetUserService, \
    SendUserRecoveryService, RecoverUserService, get_request
from ..routes import app
from ..entities.user import UserRepository
from ..utils.exceptions import \
    EmailInUseException, \
    ArgumentException, \
    AuthenticationException, \
    NoValidUserException, \
    UserValidationException, ExpiredTokenException, InvalidTokenException, UserNotFoundException

user_api = Blueprint('user_api', __name__)


@user_api.route('/create', methods=['POST'])
def create_user():
    rq = get_request(request)
    response_code = 200
    result = {}
    name = rq.get('name')
    email = rq.get('email')
    password = rq.get('password')

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
    rq = get_request(request)
    response_code = 200
    response = {}
    email = rq.get('email')
    password = rq.get('password')


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
@authenticate_user
def get_user():
    response = {}
    response_code = 200

    user_id = g.user_id

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
    rq = get_request(request)
    response = {}
    response_code = 200
    email = rq.get('email')

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
