from app.api import authenticate_user
from app.routes import app


@app.route('/<int:id>', methods=['GET'])
def get_public_profile(id):
    pass


@app.route('/', methods=["GET"])
@authenticate_user
def get_profile():
    pass


@app.route('/update', methods=["POST"])
@authenticate_user
def update_profile():
    pass
