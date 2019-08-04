from ...utils.exceptions import ArgumentException, UserValidationException, ExpiredTokenException, InvalidTokenException


class ValidateUserService:

    def __init__(self, user_repository, validation_token_verifier):
        self.user_repository = user_repository
        self.verify_validation_token = validation_token_verifier

    def call(self, args):
        if 'validation_token' not in args or args['validation_token'] is None:
            raise ArgumentException('validation token')

        validation_token = args['validation_token']

        try:
            user_email = self.verify_validation_token(validation_token)
        except ExpiredTokenException:
            raise UserValidationException('token expired')
        except InvalidTokenException:
            raise UserValidationException('invalid token')

        user = self.user_repository.get_by_email(user_email)

        if user is None:
            raise UserValidationException('user not found')

        user.validate()

        user = self.user_repository.persist(user)

        return user
