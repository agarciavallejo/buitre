from flask import Blueprint, request, jsonify
from ..services.user.userService import UserService

user_api = Blueprint('user_api',__name__)

@user_api.route('/create',methods=['POST'])
def create_user():
	name = request.form.get('name')
	email = request.form.get('email')
	password = request.form.get('password')

	args = [name, email, password]

	service = UserService()
	result = service.create(args)

	return jsonify(result)
	# Format parameters
	# Invoke CreateUser service
	# Format & return result

@user_api.route('/<int:id>',methods=['GET'])
def get_user(id):
	return "this will be a user"
