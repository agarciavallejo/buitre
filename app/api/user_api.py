from flask import Blueprint, request, jsonify
from ..services.user.createUserService import CreateUserService
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

	result = {}
	try:
		user = CreateUserService.call(args)
		result['success'] = True
	except EmailInUseException as e:
		result['error'] = e.message


	return jsonify(result)

@user_api.route('/<int:id>',methods=['GET'])
def get_user(id):
	return "this will be a user"
