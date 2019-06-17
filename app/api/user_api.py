from flask import Blueprint, request, jsonify
from ..entities.user import UserRepository, UserFactory
from ..services.user.createUserService import CreateUserService
from ..services.user.loginUserService import LoginUserService
from ..libs.exceptions import EmailInUseException, ArgumentException, AuthenticationException, NoValidUserException
from werkzeug.security import generate_password_hash

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
        user_repository = UserRepository
        user_factory = UserFactory
        service = CreateUserService(
            user_repository=user_repository,
            user_factory=user_factory,
            password_hasher=generate_password_hash
        )
        service.call(args)
        result['success'] = True
    except (EmailInUseException, ArgumentException) as e:
        result['error'] = e.message
        response_code = 500

    return jsonify(result), response_code


@user_api.route('/login', methods=['POST'])
def login_user():
    response = {}
    response_code = 200
    email = request.args['email']
    password = request.args['password']

    args = {
        'email': email,
        'password': password
    }

    try:
        token = LoginUserService.call(args)
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


@user_api.route('/<int:id>', methods=['GET'])
def get_user(id):
    return "this will be a user"
