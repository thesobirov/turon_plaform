from backend.models.basic_model import *
from app import *


@app.route(f'{api}/user_info')
@jwt_required()
def user_info():
    identity = get_jwt_identity()
    user = User.query.filter(User.id == identity).first()
    return jsonify({
        "data": user.convert_json()
    })
