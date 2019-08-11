from ...utils.exceptions import ArgumentException


class CreateOpportunityService:

    def __init__(self, opportunity_factory, opportunity_repository, picture_factory, picture_repository):
        self.opportunityFactory = opportunity_factory
        self.opportunityRepository = opportunity_repository
        self.pictureFactory = picture_factory
        self.pictureRepository = picture_repository

    def call(self, args):
        if 'user_id' not in args or args['user_id'] is None:
            raise ArgumentException('user_id parameter is mandatory')
        if 'name' not in args or args['name'] is None:
            raise ArgumentException('name parameter is mandatory')
        if 'pictures' not in args or not args['pictures']:
            raise ArgumentException('pictures parameter is mandatory and should not be empty')
        if 'latitude' not in args or not args['latitude']:
            raise ArgumentException('latitude parameter is mandatory')
        if 'longitude' not in args or not args['longitude']:
            raise ArgumentException('longitude parameter is mandatory')
        if 'address' not in args or not args['address']:
            raise ArgumentException('address parameter is mandatory')

        user_id = args['user_id']
        name = args['name']
        pictures = args['pictures']
        address = args['address']
        latitude = args['latitude']
        longitude = args['longitude']

        description = args['description'] if 'description' in args else None
        closing_date = args['closing_dat'] if 'closing_date' in args else None
        schedules = args['schedules'] if 'schedules' in args else None
        tags = args['tags'] if 'tags' in args else None

        opportunity = self.opportunityFactory.create(
            user_id,
            name,
            description,
            address,
            latitude,
            longitude,
            closing_date
        )
        opportunity = self.opportunityRepository.persist(opportunity)

        for path in pictures:
            picture = self.pictureFactory.create_for_opportunity(opportunity.id, path, user_id)
            self.pictureRepository.persist(picture)


        return opportunity
