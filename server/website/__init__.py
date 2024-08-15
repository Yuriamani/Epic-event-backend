from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

# Initialize instances
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(): 
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    cors = CORS(app, origins='*')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # JWT Configuration
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ALGORITHM'] = 'HS256'

    # In-memory blacklist store
    app.config['BLACKLIST'] = set()

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in app.config['BLACKLIST']

    app.json.compact = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    # Initialize JWT
    jwt.init_app(app)

    # Import and register Blueprints
    from .auth import auth
    from .views import views
    from .events import events
    from .tickets import tickets
    from .users import users
    from .feedbacks import feedbacks

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(events, url_prefix='/events')
    app.register_blueprint(tickets, url_prefix='/tickets')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(feedbacks, url_prefix='/feedbacks')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
