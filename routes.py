from app import app, db
from flask import request, jsonify
from models import User

# GET ALL USERS
@app.route('/api', methods=['GET'])
def get_all():

    users = User.query.all()
    result = [user.convert_to_json() for user in users]
    return jsonify(result), 200

# CREATE USER
@app.route('/api', methods=['POST'])
def create_user():
    try:

        data = request.json

        # VALIDATION
        fields = ['name','email']
        for field in fields:
            if field not in data or not data.get(field):
                return jsonify({'msg': f'Missing {field}'})

        name = data.get('name')
        email = data.get('email')

        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.convert_to_json()), 201        

    except Exception as e:

        db.session.rollback()
        return jsonify({'msg':str(e)}), 400
    
# UPDATE USER 
@app.route('/api/<int:id>', methods=['PATCH'])
def update_user(id):
    try:
        
        user = User.query.get(id)
        if user is None:
            return jsonify({'msg':'User not Found'}), 404
        
        data = request.json

        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)

        db.session.commit()
        return jsonify(user.convert_to_json()), 200


    except Exception as e:

        db.session.rollback()
        return jsonify({'msg':str(e)}), 500