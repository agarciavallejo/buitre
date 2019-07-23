from ...utils.exceptions import ArgumentException, EmailInUseException
from ...utils.email import EmailFactory, EmailSender


class CreateUserService:

    def __init__(self, user_repository, user_factory, password_hasher, validation_token_generator):
        self.userRepository = user_repository
        self.userFactory = user_factory
        self.hash_password = password_hasher
        self.generate_validation_token = validation_token_generator

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

        hashed_password = self.hash_password(raw_password)
        user = self.userFactory.create(name, email, hashed_password)
        validation_token = self.generate_validation_token(email)
        user.validation_token = validation_token

        self.userRepository.persist(user)
        persisted_user = self.userRepository.get_by_email(email)

        validation_email = EmailFactory.create_user_validation_email(user.name, user.email, validation_token)
        EmailSender.send(validation_email)

        return persisted_user
