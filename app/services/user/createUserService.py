from ...libs.exceptions import ArgumentException, EmailInUseException
from werkzeug.security import generate_password_hash


class CreateUserService:

    def __init__(self, user_repository, user_factory):
        self.userRepository = user_repository
        self.userFactory = user_factory

    def call(self, args):

        if 'email' not in args or args['email'] is None:
            raise ArgumentException('email')
        if 'name' not in args or args['name'] is None:
            raise ArgumentException('name')
        if 'password' not in args or args['password'] is None:
            raise ArgumentException('password')

        name = args['name']
        email = args['email']
        raw_password = args['password']

        if self.userRepository.get_by_email(email) is not None:
            raise EmailInUseException()

        hashed_password = generate_password_hash(raw_password)

        user = self.userFactory.create(name, email, hashed_password)
        self.userRepository.persist(user)
