from flask import g, jsonify, Blueprint, request

from ..api import authenticate_user, GetProfileService, UpdateProfileService

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
    response.pop('email', None)
    response_code = 200

    return jsonify(response), response_code


@profile_api.route('/update', methods=["POST"])
@authenticate_user
def update_profile():

    user_id = g.user_id

    args = {
        'user_id': user_id
    }

    if request.form.get('name'):
        args['name'] = request.form.get('name')
    if request.form.get('latitude'):
        args['latitude'] = request.form.get('latitude')
    if request.form.get('longitude'):
        args['longitude'] = request.form.get('longitude')
    if request.form.get('radius'):
        args['radius'] = request.form.get('radius')
    if request.form.get('profile_picture'):
        args['profile_picture'] = request.form.get('profile_picture')

    UpdateProfileService.call({args})

    return jsonify({'message': "OK"}), 200
