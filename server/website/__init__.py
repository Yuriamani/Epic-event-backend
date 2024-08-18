from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

# Initialize instances
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(): 
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    CORS(app, origins='*')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT Configuration
    app.config['JWT_ALGORITHM'] = 'HS256'
    app.config['BLACKLIST'] = set()

    # Import models (User) here or after initializing extensions
    from .models import User

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in app.config['BLACKLIST']

    @app.route('/auth/user-info', methods=['GET'])
    @jwt_required()
    def user_info():
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user['id']).first()
        if user:
            return jsonify({
                "username": user.username,
                "email": user.email
            }), 200
        return jsonify({"message": "User not found"}), 404

    @app.route('/auth/update-user-info', methods=['POST'])
    @jwt_required()
    def update_user_info():
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user['id']).first()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.get_json()
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'newPassword' in data and data['newPassword']:
            user.password = generate_password_hash(data['newPassword'])

        db.session.commit()
        return jsonify({'message': 'User info updated successfully'}), 200

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import and register Blueprints
    from .auth import auth
    from .views import views
    from .events import events
    from .tickets import tickets
    from .users import users

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(events, url_prefix='/events')
    app.register_blueprint(tickets, url_prefix='/tickets')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
