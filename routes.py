from app import app, db
from flask import request, jsonify
from models import User

# GET ALL USERS
@app.route('/api', methods=['GET'])
def get_all():

    users = User.query.all()
    result = [user.convert_to_json() for user in users]
    return jsonify(result), 200