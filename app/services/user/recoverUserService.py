from ...utils.exceptions import ArgumentException, ExpiredTokenException, InvalidTokenException, AuthenticationException


class RecoverUserService:

    def __init__(self, token_verifier, user_repository, password_hasher):
        self.verify_token = token_verifier
        self.user_repository = user_repository
        self.hash_password = password_hasher

    def call(self, args):
        if 'recovery_token' not in args or args['recovery_token'] is None:
            raise ArgumentException('missing recovery_token argument')
        if 'password' not in args or args['password'] is None:
            raise ArgumentException('missing password argument')

        recovery_token = args['recovery_token']
        password = args['password']

        try:
            user_email = self.verify_token(recovery_token)
        except (InvalidTokenException, ExpiredTokenException) as e:
            raise e

        if user_email is None:
            raise InvalidTokenException()

        user = self.user_repository.get_by_email(user_email)

        if user is None:
            raise AuthenticationException()

        user.password = self.hash_password(password)
        self.user_repository.persist(user)

        return user



