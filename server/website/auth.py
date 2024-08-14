from website import db, login_manager
from flask import Blueprint, request, jsonify, redirect, url_for
from .models import User
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
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user') # Default role is 'user'

        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'User already exists'}), 400

        new_user = User(email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created'}), 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200
        return jsonify({'message': 'Invalid credentials'}), 401 

class UserLogout(Resource):
    @login_required
    def post(self):
        logout_user()
        return redirect(url_for('login'))

class AdminEvent(Resource):
    @login_required
    def post(self):
        if current_user.role != 'admin':
            return jsonify({'message': 'Access forbidden'}), 403
        
        # Logic to create an event
        return {'message': 'Event created'}, 201

    @login_required
    def delete(self):
        if current_user.role != 'admin':
            return jsonify({'message': 'Access forbidden'}), 403
        
        # Logic to delete an event
        return {'message': 'Event deleted'}, 200    

api.add_resource(UserSignUp, '/signup')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(AdminEvent, '/events')
