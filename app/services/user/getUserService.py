from ...utils.exceptions import ArgumentException, UserNotFoundException


class GetUserService():

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def call(self, args):
        if 'user_id' not in args or args['user_id'] is None:
            raise ArgumentException('missing user_id parameter')

        user_id = args['user_id']

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException('user ' + str(user_id) + ' not found')

        return user.to_dict()
