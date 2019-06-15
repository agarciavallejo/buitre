from ...libs.exceptions import AuthenticationException, ArgumentException, NoValidUserException
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

		if(user is None or not check_password_hash(user.password,password)):
			raise AuthenticationException()
		if(not user.is_valid):
			raise NoValidUserException()

		return 'this-is-a-session-token'