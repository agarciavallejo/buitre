from ...utils.exceptions import ArgumentException, AuthenticationException


class SendUserRecoveryService:

    def __init__(self, user_repository, email_factory, email_sender, token_generator):
        self.user_repository = user_repository
        self.email_factory = email_factory
        self.email_sender = email_sender
        self.generate_token = token_generator

    def call(self, args):
        if 'email' not in args or args['email'] is None:
            raise ArgumentException('Email is required')

        email = args['email']

        user = self.user_repository.get_by_email(email)
        if user is None:
            raise AuthenticationException()

        recovery_token = self.generate_token(email)

        email = self.email_factory.create_recovery_email(user.name, user.email, recovery_token)
        self.email_sender.send(email)

        return True
