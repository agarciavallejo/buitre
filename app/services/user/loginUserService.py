from ...libs.exceptions.argumentException import ArgumentException
from werkzeug.security import check_password_hash

class LoginUserService:

	@staticmethod
	def call(args):
		if ('email' not in args or args['email'] is None):
			raise ArgumentException('email')
		if ('password' not in args or args['password'] is None):
			raise ArgumentException('password')

		email = args['email']
		password = args['password']

		user = User.getByEmail(email)

		if(user is None):
			return None
		if(not check_password_hash(user.password,password))
			return None

		return 'this-is-a-session-token'