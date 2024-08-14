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
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')
        role = data.get('role', 'user') # Default role is 'user'

        if User.query.filter_by(email=email).first():
            return {'message': 'User already exists'}, 400
        elif len(email) < 4:
            {'error': 'must be greater than 3 characters'}, 400
        elif len(username) < 2:
            {'error': 'Username must be greater than 1 character'}, 400
        elif password1 != password2:
            {'error': 'passwords don\'t match'}, 400
        elif len(password1) < 7:
            {'error': 'Passwords must be atleast 7 characters'}, 400
        else:
            new_user = User(email=email, role=role, username=username, password=generate_password_hash(
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
                return {'user': {'id': user.id, 'email': user.email}}
            else:
                {'error': 'Incorrect password'}, 401
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
