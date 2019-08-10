from ...utils.exceptions import ArgumentException, UserNotFoundException


class GetProfileService:

    def __init__(self, user_repository, comment_repository, opportunity_repository, tag_repository, picture_repository):
        self.user_repository = user_repository
        self.comment_repository = comment_repository
        self.opportunity_repository = opportunity_repository
        self.tag_repository = tag_repository
        self.picture_repository = picture_repository

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
            radius=user.radius,
            picture=user.profile_picture
        )
        # TODO: add profile picture when implemented

        profile_data['tags'] = self.get_tags(user_id)
        profile_data['opportunities'] = self.get_opportunities(user_id)
        profile_data['favorited_opportunities'] = self.get_favorited_opportunities(user_id)
        profile_data['contributions'] = self.get_contributions(user_id)

        return profile_data

    def get_tags(self, user_id):
        tags = []
        for t in self.tag_repository.get_by_user_id(user_id):
            tag = dict(
                name=t.name,
                id=t.id
            )
            tags.append(tag)
        return tags

    def get_opportunities(self, user_id):
        opportunities = []
        for o in self.opportunity_repository.get_by_user_id(user_id):
            opportunity = {
                'name': o.name,
                'id': o.id,
                'picture': ""
            }

            pictures = self.picture_repository.get_by_opportunity_id(o.id)
            if len(pictures):
                opportunity['picture'] = pictures[0].path

            opportunities.append(opportunity)
        return opportunities

    def get_favorited_opportunities(self, user_id):
        favorited_opportunities = []
        for fav in self.opportunity_repository.get_by_liked_by(user_id):
            opportunity = dict(
                id=fav.id,
                name=fav.name,
                picture=""
            )

            pictures = self.picture_repository.get_by_opportunity_id(fav.id)
            if len(pictures):
                opportunity['picture'] = pictures[0].path

            favorited_opportunities.append(opportunity)
        return favorited_opportunities

    def get_contributions(self, user_id):
        contributions = []
        for c in self.comment_repository.get_by_user_id(user_id):
            comment = dict(
                type="comment",
                text=c.text,
                opportunity_id=c.opportunity_id,
                score=c.score,
                created_at=c.created_at
            )
            opportunity = self.opportunity_repository.get_by_id(c.opportunity_id)
            comment['opportunity_name'] = opportunity.name
            contributions.append(comment)
            # TODO: add other contributions like corrections to opportunities

        return contributions
