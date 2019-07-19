from ...libs.exceptions import ArgumentException, UserValidationException


class ValidateUserService:

    def __init__(self, user_repository, validation_token_verifier):
        self.user_repository = user_repository
        self.verify_validation_token = validation_token_verifier

    def call(self, args):
        if 'validation_token' not in args or args['validation_token'] is None:
            raise ArgumentException('validation token')

        validation_token = args['validation_token']

        user = self.user_repository.get_by_validation_token(validation_token)

        if user is None:
            raise UserValidationException('user not found')

        if self.verify_validation_token(validation_token):
            user.validate()
        else:
            raise UserValidationException('token expired')

        self.user_repository.persist(user)

        return user
