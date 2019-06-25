from ...libs.exceptions import ArgumentException, UserValidationException


class ValidateUserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def call(self, args):
        if 'id' not in args or args['id'] is None:
            raise ArgumentException('user id')

        user_id = args['id']

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserValidationException('user not found')

        user = self.user_repository.validate(user_id)

        return user
