# from flask import Flask, request, jsonify
# from flask_restful import Api, Resource, reqparse
# from flask_login import LoginManager, UserMixin, login_user, logout_user
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField
# from wtforms.validators import InputRequired, Length, Email
# from flask_bcrypt import Bcrypt
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from flask import Flask
from website.views import views
from website.events import events
from website.tickets import tickets
from website.users import users
from website.feedbacks import feedbacks
from website.models import db
from flask_migrate import Migrate
# import os
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


# from flask import Flask, request, jsonify
# from flask_restful import Api, Resource, reqparse
# from flask_login import LoginManager, UserMixin, login_user, logout_user
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField
# from wtforms.validators import InputRequired, Length, Email
# from flask_bcrypt import Bcrypt
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret_key_here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://...'

# api = Api(app)
# bcrypt = Bcrypt(app)
# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["200 per day", "50 per hour"]
# )

# class User(UserMixin):
#     def __init__(self, username, password):
#         self.username = username
#         self.password = bcrypt.generate_password_hash(password)

#     def check_password(self, password):
#         return bcrypt.check_password_hash(self.password, password)

# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# class Login(Resource):
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('username', type=str, required=True, help='Username is required')
#         parser.add_argument('password', type=str, required=True, help='Password is required')
#         args = parser.parse_args()

#         user = User.query.filter_by(username=args['username']).first()
#         if user and user.check_password(args['password']):
#             login_user(user)
#             return {'message': 'Logged in successfully'}, 200
#         return {'message': 'Invalid username or password'}, 401

# class Logout(Resource):
#     def post(self):
#         logout_user()
#         return {'message': 'Logged out successfully'}, 200

# class Register(Resource):
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('username', type=str, required=True, help='Username is required')
#         parser.add_argument('password', type=str, required=True, help='Password is required')
#         args = parser.parse_args()

#         user = User(args['username'], args['password'])
#         db.session.add(user)
#         db.session.commit()
#         return {'message': 'User created successfully'}, 201

# class Events(Resource):
#     @limiter.limit("10 per minute")
#     def get(self):
#         events = Event.query.all()
#         return [{'id': event.id, 'name': event.name} for event in events]

# api.add_resource(Login, '/login')
# api.add_resource(Logout, '/logout')
# api.add_resource(Register, '/register')
# api.add_resource(Events, '/events')

# if __name__ == '__main__':
#     app.run(debug=True)    