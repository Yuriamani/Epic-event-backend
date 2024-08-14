from . import db, login_manager
from flask import Blueprint, request, jsonify, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import validate_request_data, handle_error
from flask_restful import Api, Resource
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)
api = Api(auth)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
            login_user(new_user, remember=True)
            return {'message': 'Account Created'}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return {"message": "Logged in successfully"}
            else:
                return {'error': 'Incorrect password'}, 401
        else:
            return {'error': 'Email does not exist'}, 404

class UserLogout(Resource):
    @login_required
    def post(self):
        logout_user()
        return {"message": "Logged out successfully"}  

api.add_resource(UserSignUp, '/signup')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
