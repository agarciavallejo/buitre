from ...libs.exceptions import ArgumentException, EmailInUseException
from ...libs.email import EmailFactory, EmailSender


class CreateUserService:

    def __init__(self, user_repository, user_factory, password_hasher):
        self.userRepository = user_repository
        self.userFactory = user_factory
        self.password_hasher = password_hasher

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

        hashed_password = self.password_hasher(raw_password)
        user = self.userFactory.create(name, email, hashed_password)

        self.userRepository.persist(user)
        persisted_user = self.userRepository.get_by_email(email)

        print(persisted_user)
        validation_email = EmailFactory.create_user_validation_email(user.name, user.email, persisted_user.id)
        EmailSender.send(validation_email)

        return persisted_user
