from ...utils.exceptions import ArgumentException


class UpdateProfileService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def call(self, args):
        if 'user_id' not in args or args['user_id'] is None:
            raise ArgumentException('user_id argument is required')

        user_id = args['user_id']
        user = self.user_repository.get_by_id(user_id)

        if 'name' in args and args['name'] is not None and args['name'] != user.name:
            user.name = args['name']
        if 'latitude' in args and args['latitude'] is not None and args['latitude'] != user.latitude:
            user.latitude = args['latitude']
        if 'longitude' in args and args['longitude'] is not None and args['longitude'] != user.longitude:
            user.longitude = args['longitude']
        if 'radius' in args and args['radius'] is not None and args['radius'] != user.radius:
            user.radius = args['radius']
        if 'profile_picture' in args and args['profile_picture'] is not None and args['profile_picture'] != user.profile_picture:
            user.profile_picture = args['profile_picture']

        user = self.user_repository.persist(user)

        return user.to_dict()
