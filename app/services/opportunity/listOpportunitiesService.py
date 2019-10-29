from ...utils.exceptions import ArgumentException


class ListOpportunitiesService:

    def __init__(self, opportunity_repository):
        self.opportunity_repository = opportunity_repository
        self.mandatory_params = ['keywords', 'page']
        self.PAGE_SIZE = 10

    def call(self, args):
        for param in self.mandatory_params:
            if param not in args:
                raise ArgumentException('missing "' + param + '" parameter')

        keywords = args['keywords']
        page = args['page']

        db_opportunities = self.opportunity_repository.execute_query(keywords, self.PAGE_SIZE, page)

        results = []
        for db_opportunity in db_opportunities:
            results.append(db_opportunity.to_dict())

        return results
