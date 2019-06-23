from ...libs.exceptions import AuthenticationException, ArgumentException, NoValidUserException


class LoginUserService:

    def __init__(self, user_repository, token_generator, hash_checker_func):
        self.user_repository = user_repository
        self.token_generator = token_generator
        self.hash_checker_func = hash_checker_func

    def call(self, args):
        if 'email' not in args or args['email'] is None:
            raise ArgumentException('email')
        if 'password' not in args or args['password'] is None:
            raise ArgumentException('password')

        email = args['email']
        password = args['password']

        user = self.user_repository.get_by_email(email)

        if user is None or not self.hash_checker_func(user.password, password):
            raise AuthenticationException()
        if not user.has_been_validated():
            raise NoValidUserException()

        login_token = self.token_generator.generate_login_token({'data': user.id})
        user.login_token = login_token
        self.user_repository.persist(user)

        return login_token
