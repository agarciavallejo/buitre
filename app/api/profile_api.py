from flask import g, jsonify

from ..api import authenticate_user, GetProfile
from ..routes import app


@app.route('/<int:id>', methods=['GET'])
def get_public_profile(id):
    pass


@app.route('/', methods=["GET"])
@authenticate_user
def get_profile():
    user_id = g.user_id

    response = GetProfile({'user_id': user_id})
    response_code = 200

    return jsonify(response), response_code


@app.route('/update', methods=["POST"])
@authenticate_user
def update_profile():
    pass
