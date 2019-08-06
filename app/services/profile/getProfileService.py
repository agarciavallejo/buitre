from ...utils.exceptions import ArgumentException, UserNotFoundException


class GetProfile:

    def __init__(self, user_repository, comment_repository, opportunity_repository):
        self.user_repository = user_repository
        self.comment_repository = comment_repository
        self.opportunity_repository = opportunity_repository

    def call(self, args):
        if 'user_id' not in args:
            raise ArgumentException("missing user_id argument")

        user_id = args['user_id']

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException('user ' + str(user_id) + ' not found')

        profile_data = dict(
            name=user.name,
            email=user.email,
            score=user.score,
            latitude=user.latitude,
            longitude=user.longitude,
            radius=user.radius
        )
        # TODO: add profile picture when implemented

        tags = []
        profile_data['tags'] = tags

        opportunities = []
        for o in self.opportunity_repository.get_by_user_id(user_id):
            opportunity = {
                'name': o.name,
                'id': o.id
            }
            opportunities.append(opportunity)
        profile_data['opportunities'] = opportunities

        favorites = []
        profile_data['favorited_opportunities'] = favorites

        contributions = []
        for c in self.comment_repository.get_by_user_id(user_id):
            comment = dict(
                type="comment",
                text=c.text,
                opportunity_id=c.opportunity_id,
                created_at=c.created_at
            )
            opportunity = self.opportunity_repository.get_by_id(c.opportunity_id)
            comment['opportunity_name'] = opportunity.name
            contributions.append(comment)
            # TODO: add other contributions like corrections to opportunities

        profile_data['contributions'] = contributions



        return profile_data
