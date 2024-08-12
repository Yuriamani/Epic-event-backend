from flask import Blueprint, request, jsonify
from .models import db, User
from .utils import validate_request_data, handle_error, validate_email
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash

users = Blueprint('users', __name__)
api = Api(users)

class Users(Resource):
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users], 200

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
        user = User(username=data['username'], email=data['email'], password_hash=password_hash)
        
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201
    
    def patch(self):
        data = request.json

        user = User.query.get(id)
        if user is None:
            return {'error': 'User not found'}, 404

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
    
    def delete(self):
        data = request.json
        id = data.get('id')
        if id is None:
            return {'error': 'Missing user ID'}, 400

        user = User.query.get(id)
        if user is None:
            return {'error': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200

api.add_resource(Users, '/users')

class UserLogin(Resource):
    def post(self):
        data = request.json
        username_or_email = data.get('username') or data.get('email')
        password = data.get('password')

        if not username_or_email or not password:
            return handle_error('Missing username/email or password', 400)

        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if user and check_password_hash(user.password_hash, password):
            return jsonify({'message': 'Login successful'}), 200
        else:
            return handle_error('Invalid username, email, or password', 401)

api.add_resource(UserLogin, '/users/login')
   