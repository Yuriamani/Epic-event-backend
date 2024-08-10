from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from os import path
# from flask_login import LoginManager
from website.views import views
from website.events import events
from website.tickets import tickets
from website.users import users
from website.feedbacks import feedbacks
from website.models import db
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)
db.init_app(app)

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(events, url_prefix='/')
app.register_blueprint(tickets, url_prefix='/')
app.register_blueprint(users, url_prefix='/')
app.register_blueprint(feedbacks, url_prefix='/')

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))

if __name__ == '__main__':
    app.run(debug=True)