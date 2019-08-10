from flask import Blueprint, request, jsonify

from ..api import GetOpportunityService
from ..utils.exceptions import OpportunityNotFoundException

opportunity_api = Blueprint('opportunity_api', __name__)


@opportunity_api.route('/<int:opportunity_id>', methods=['GET'])
def get_opportunity(opportunity_id):
    response = {}
    response_code = 200

    try:
        response = GetOpportunityService.call({
            'opportunity_id': opportunity_id
        })
    except OpportunityNotFoundException as e:
        response['message'] = e.message
        response_code = 404

    return jsonify(response), response_code
