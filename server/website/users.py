from flask import Blueprint, request
from .models import db, User
from .utils import validate_request_data, handle_error
from flask_restful import Api, Resource

users = Blueprint('users', __name__)
api = Api(users)

class Users(Resource):
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    def post(self):
        data = request.json
        required_fields = ['username', 'email', 'password_hash']
        if not validate_request_data(data, required_fields):
            return handle_error('Missing required fields', 400)
        user = User(username=data['username'], email=data['email'],password_hash=data['password_hash'])
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201
    
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
            user.email = data['email']
        if 'password_hash' in data:
            user.password_hash = data['password_hash']

        db.session.commit()
        return user.to_dict(), 200
    
    def delete(self):
        data = request.json
        id = data.get('id')
        if id is None:
            return {'error': 'Missing user ID'}, 400

        user = User.query.get(id)
        if user is None:
            return {'error': 'user not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message': 'user deleted successfully'}, 200

api.add_resource(Users, '/users')    