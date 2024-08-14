from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
# import os
# Initialize instances
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = 'yuriamani7'
    cors = CORS(app, origins='*')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://epic_events_h3bm_user:ykU3suwVensjbDjqsCfnBapwB4DBp1Pa@dpg-cqu51ebv2p9s73d0sfg0-a.frankfurt-postgres.render.com/epic_events_h3bm'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

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
