from ...utils.exceptions import ArgumentException


class ListOpportunitiesService:

    def __init__(self, opportunityRepository):
        self.opportunityRepository = opportunityRepository
        self.mandatory_params = ['lat', 'lng', 'keywords', 'filters']

    def call(self, args):
        for param in self.mandatory_params:
            if param not in args:
                raise ArgumentException('missing "' + param + '" parameter')

        lat = args['lat']
        lng = args['lng']
        keywords = args['keywords']
        filters = args['filters']

        self.opportunityRepository.initQuery()
        if lat is not None and lng is not None:
            self.opportunityRepository.centerQuery(lat, lng)

        if keywords:
            self.opportunityRepository.addKeyworkdsToQuery(keywords)

        if len(filters):
            for filter, value in filters:
                self.opportunityRepository.addFilterToQuery(filter, value)

        db_opportunities = self.opportunityRepository.executeQuery()

        results = []
        for db_opportunity in db_opportunities:
            opportunity = {
                'id': db_opportunity.id,
                'name': db_opportunity.name,
            }
            results.append(opportunity)

        return results
