from ...utils.exceptions import AuthenticationException, ArgumentException, NoValidUserException


class LoginUserService:

    def __init__(self, user_repository, token_generator, hash_checker):
        self.user_repository = user_repository
        self.generate_session_token = token_generator
        self.check_hash = hash_checker

    def call(self, args):
        if 'email' not in args or args['email'] is None:
            raise ArgumentException('email')
        if 'password' not in args or args['password'] is None:
            raise ArgumentException('password')

        email = args['email']
        password = args['password']

        user = self.user_repository.get_by_email(email)

        if user is None or not self.check_hash(user.password, password):
            raise AuthenticationException()
        if not user.has_been_validated():
            raise NoValidUserException()

        session_token = self.generate_session_token(user.id)
        user.session_token = session_token
        self.user_repository.persist(user)

        return session_token
