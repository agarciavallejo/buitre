from flask import g, jsonify, Blueprint, request

from ..api import authenticate_user, GetProfileService, UpdateProfileService, UpdateUserTagsService, get_request

profile_api = Blueprint('profile_api', __name__)


@profile_api.route('/', methods=["GET"])
@authenticate_user
def get_profile():
    user_id = g.user_id

    response = GetProfileService.call({'user_id': user_id})
    response_code = 200

    return jsonify(response), response_code


@profile_api.route('/<int:id>', methods=['GET'])
def get_public_profile(id):
    response = GetProfileService.call({'user_id': id})

    # remove private information
    response.pop('email', None)
    response.pop('latitude', None)
    response.pop('longitude', None)
    response.pop('radius', None)

    response_code = 200

    return jsonify(response), response_code


@profile_api.route('/update', methods=["POST"])
@authenticate_user
def update_profile():
    rq = get_request(request)
    user_id = g.user_id

    args = {
        'user_id': user_id
    }

    if rq.get('name'):
        args['name'] = rq.get('name')
    if rq.get('latitude'):
        args['latitude'] = rq.get('latitude')
    if rq.get('longitude'):
        args['longitude'] = rq.get('longitude')
    if rq.get('radius'):
        args['radius'] = rq.get('radius')
    if rq.get('profile_picture'):
        args['profile_picture'] = rq.get('profile_picture')

    UpdateProfileService.call(args)

    return jsonify({'message': "OK"}), 200


@profile_api.route('/update/tags', methods=["POST"])
@authenticate_user
def update_tags():
    rq = get_request(request)
    user_id = g.user_id

    tags = rq.get('tags').split(",")

    UpdateUserTagsService.call({'user_id': user_id, 'tags': tags})

    return jsonify({'message': "OK"}), 200
