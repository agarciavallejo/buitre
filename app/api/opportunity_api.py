from flask import Blueprint, request, jsonify, g

from ..api import GetOpportunityService, CreateOpportunityService, authenticate_user, get_request
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


@opportunity_api.route('/create', methods=['POST'])
@authenticate_user
def create_opportunity():
    rq = get_request(request)
    response = {}
    response_code = 200

    tags = rq.get('tags').split(',')
    pictures = rq.get('pictures').split(',')

    args = {
        'user_id': g.user_id,
        'name': rq.get('name'),
        'description': rq.get('description'),
        'address': rq.get('address'),
        'latitude': rq.get('latitude'),
        'longitude': rq.get('longitude'),
        'pictures': pictures,
        'tags': tags
    }

    try:
        CreateOpportunityService.call(args)
        response['message'] = "success"
    except Exception as e:
        response['message'] = e.message
        response_code = 500

    return jsonify(response), response_code
