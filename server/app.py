from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from os import path
# from flask_login import LoginManager
from .website.views import views
from .website.events import events
from .website.tickets import tickets
from .website.users import users
from .website.feedbacks import feedbacks
from .website.models import db
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
cors = CORS(app, origins='*')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://epic_events_z6wl_user:CndecxpLEos242Bi80iODMgrvMSoymqC@dpg-cqplpv5svqrc73fu470g-a.oregon-postgres.render.com/epic_events_z6wl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)
db.init_app(app)

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(events, url_prefix='/events')
app.register_blueprint(tickets, url_prefix='/tickets')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(feedbacks, url_prefix='/feedbacks')

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))

if __name__ == '__main__':
    app.run(debug=True)