from flask import Flask
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

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(events, url_prefix='/events')
app.register_blueprint(tickets, url_prefix='/tickets')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(feedbacks, url_prefix='/feedbacks')

if __name__ == '__main__':
    app.run(debug=True)
