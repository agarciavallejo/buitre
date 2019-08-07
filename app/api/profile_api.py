from flask import g, jsonify, Blueprint

from ..api import authenticate_user, GetProfileService

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
    pass
