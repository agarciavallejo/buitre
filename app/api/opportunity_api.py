from flask import Blueprint, request, jsonify

from ..routes import app
from ..entities.opportunity import OpportunityRepository
from ..services.opportunity.getOpportunityService import GetOpportunityService
from ..utils.exceptions import ArgumentException, OpportunityNotFoundException

opportunity_api = Blueprint('opportunity_api', __name__)

# Instantiate services
GetOpportunityService = GetOpportunityService(
    opportunity_repository = OpportunityRepository
)

@opportunity_api.route('/get', methods=['GET'])
def get_opportunity():
    response = {}
    response_code = 200

    opportunity_id = request.args.get('opportunity_id')
       
    try:
        response = GetOpportunityService.call({
            'opportunity_id': opportunity_id
        })
    except OpportunityNotFoundException as e:
        response['message'] = e.message

        response_code = 500

    return jsonify(response), response_code
