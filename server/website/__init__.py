from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

# Initialize instances
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(): 
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    cors = CORS(app, origins='*')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT Configuration
    app.config['JWT_ALGORITHM'] = 'HS256'

    # In-memory blacklist store
    app.config['BLACKLIST'] = set()

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in app.config['BLACKLIST']
    
    @app.route('/verify-token', methods=['GET'])
    @jwt_required()
    def verify_token():
       user_identity = get_jwt_identity()
       return jsonify(user_identity=user_identity), 200

    app.json.compact = False

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
    # Remove the feedbacks import if no longer needed
    # from .feedbacks import feedbacks

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(events, url_prefix='/events')
    app.register_blueprint(tickets, url_prefix='/tickets')
    app.register_blueprint(users, url_prefix='/users')
    # app.register_blueprint(feedbacks, url_prefix='/feedbacks')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
