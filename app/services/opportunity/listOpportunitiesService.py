class ListOpportunitiesService:

    def __init__(self, opportunityRepository):
        self.opportunityRepository = opportunityRepository

    def call(self, args):

        query = args['query']

        db_opportunities = self.opportunityRepository.search(lat, lng, query)

        results = []
        for db_opportunity in db_opportunities:
            opportunity = {
                'id': db_opportunity.id,
                'name': db_opportunity.name,

            }
            results.append(opportunity)

        return results
