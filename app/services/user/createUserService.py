from ...entities.user import User
from ...libs.exceptions import ArgumentException, EmailInUseException
from werkzeug.security import generate_password_hash

class CreateUserService:

	@staticmethod
	def call(args):
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
			raise EmailInUseException()

		hashed_password = generate_password_hash(raw_password)

		user = User(name, email, hashed_password)
		user.is_valid = False
		user.persist()