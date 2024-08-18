from flask import Blueprint, request
from . import db
from .models import User
from .utils import validate_request_data, handle_error, validate_email
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

users = Blueprint('users', __name__)
api = Api(users)

class UserData(Resource):
    @jwt_required()
    # current_user = get_jwt_identity()
        # if current_user.role != 'admin':
        #     return jsonify({'message': 'Access forbidden'}), 403
    def delete(self,id):
        if id is None:
            return {'error': 'Missing user ID'}, 400

        user = User.query.get(id)
        if user is None:
            return {'error': 'user not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message': 'user deleted successfully'}, 200
    
class Users(Resource):
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    @jwt_required()
    def post(self):
        data = request.json
        required_fields = ['username', 'email', 'password']
        if not validate_request_data(data, required_fields):
            return handle_error('Missing required fields', 400)
        email = data.get('email')
        if not validate_email(email):
            return handle_error('Invalid email format', 400)
        password = data.get('password')
        password_hash = generate_password_hash(password)
        user = User(username=data['username'], email=data['email'],password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201
    
    @jwt_required()
    def patch(self):
        data = request.json
        id = data.get('id')
        if id is None:
            return {'error': 'Missing user ID'}, 400

        user = User.query.get(id)
        if user is None:
            return {'error': 'user not found'}, 404

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            email = data.get('email')
            if not validate_email(email):
                return handle_error('Invalid email format', 400)
            user.email = email
        if 'password' in data:
            password = data.get('password')
            password_hash = generate_password_hash(password)
            user.password_hash = password_hash

        db.session.commit()
        return user.to_dict(), 200

api.add_resource(Users, '/users')
api.add_resource(UserData, '/users/<int:id>')    