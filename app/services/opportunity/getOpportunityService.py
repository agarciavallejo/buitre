from ...utils.exceptions import ArgumentException, OpportunityNotFoundException


class GetOpportunityService:

    def __init__(self, opportunity_repository):
        self.opportunity_repository = opportunity_repository

    def call(self, args):
        if 'opportunity_id' not in args or args['opportunity_id'] is None:
            raise ArgumentException('missing opportunity_id parameter')

        opportunity_id = args['opportunity_id']

        opportunity = self.opportunity_repository.get_by_id(opportunity_id)

        if opportunity is None:
            raise OpportunityNotFoundException('opportunity ' + str(opportunity_id) + ' not found')

        return opportunity.to_dict()
