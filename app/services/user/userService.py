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

		name = args['name']
		email = args['email']
		raw_password = args['password']

		if (User.getByEmail(email) is not None):
			raise Exception('email already in use')

		user = User(name, email, hashed_password)
		user.persist()

		return user 