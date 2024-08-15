from . import db
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt_identity, get_jwt
from flask import Blueprint, request, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import validate_request_data, handle_error
from flask_restful import Api, Resource
import jwt
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)
api = Api(auth)

class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {'access_token': new_access_token}

class UserSignUp(Resource):
    def post(self):
        data = request.json
        required_fields = ['username', 'email', 'password1', 'password2', 'role']
        if not validate_request_data(data, required_fields):
            return handle_error('Missing required fields', 400)
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')
        role = data.get('role', 'user')  # Default role is 'user'

        if password1 != password2:
            return handle_error('Passwords do not match', 400)

        if role not in ['user', 'admin']:
            return handle_error('Invalid role', 400)

        if User.query.filter_by(email=email).first():
            return {'message': 'User already exists'}, 400
        else:
            new_user = User(email=data['email'], role=role, username=data['username'], password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'Account Created'}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                access_token = create_access_token(identity=username)
                refresh_token = create_refresh_token(identity=username)
                return {'access_token': access_token, 'refresh_token': refresh_token}
            else:
                return {'error': 'Incorrect password'}, 401
        else:
            return {'error': 'Email does not exist'}, 404

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']  # Get the JWT ID
        blacklist = request.app.config['BLACKLIST']
        blacklist.add(jti)  # Add the token ID to the blacklist
        return {"message": "Logged out successfully"}  

api.add_resource(UserSignUp, '/signup')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(RefreshToken, '/refresh')
