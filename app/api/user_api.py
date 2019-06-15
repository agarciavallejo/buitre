from flask import Blueprint, request, jsonify
from ..services.user.createUserService import CreateUserService
from ..services.user.loginUserService import LoginUserService
from ..entities.user import User
from ..libs.exceptions.emailInUseException import EmailInUseException

user_api = Blueprint('user_api',__name__)

@user_api.route('/create',methods=['POST'])
def create_user():
	name = request.form.get('name')
	email = request.form.get('email')
	password = request.form.get('password')

	args = {
		'name': name, 
		'email': email, 
		'password': password
	}

	response_code = 200
	result = {}
	try:
		CreateUserService.call(args)
		result['success'] = True
	except EmailInUseException as e:
		result['error'] = e.message
		response_code = 500

	return jsonify(result), response_code


@user_api.route('/login', methods=['POST'])
def login_user():
	email = request.args['email']
	password = request.args['password']

	args = {
		'email': email,
		'password': password
	}

	token = LoginUser.call(args)
	if(token is None):
		result['error'] = 'authentication failed'
	else:
		result['token'] = token

	return jsonify(result), 200


@user_api.route('/<int:id>',methods=['GET'])
def get_user(id):
	return "this will be a user"
