from flask_resful import Api, Resource
from .services.user import GetUser, createUser, deleteUser

class RestUser(Resource):
	def get(self, user_id):
		return getUser(user_id)

	def put(self, args):
		return createUser(args)

	def delete(self, user_id):
		return deleteUser(args)
