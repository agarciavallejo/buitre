from ...lib.exceptions.argumentException import ArgumentException
from ...entities.user import User

class UserService:

	def create(self, args):
		print(args)
		if ('email' not in args or args['email'] is None):
			raise ArgumentException('email')
		if ('name' not in args or args['name'] is None):
			raise ArgumentException('name')
		if ('password' not in args or args['password'] is None):
			raise ArgumentException('password')

		user = User(args['name'], args['email'], args['password'])
		user.persist()

		return user 