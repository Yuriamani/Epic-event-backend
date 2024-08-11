from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, Event, UserEvent, Feedback, Ticket, EventOrganizer
from flask_cors import CORS
import os

app = Flask(__name__)
os.environ['DATABASE_URL'] = 'postgresql://epic_events_z6wl_user:CndecxpLEos242Bi80iODMgrvMSoymqC@dpg-cqplpv5svqrc73fu470g-a.oregon-postgres.render.com/epic_events_z6wl'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
CORS(app, origins='*')

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Events RESTful API",
        }
        return make_response(response_dict, 200)

class Users(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        users = User.query.all()
        return {"count": len(users), "users": [user.to_dict() for user in users]}, 200

    def post(self):
        email = User.query.filter_by(email=request.json.get('email')).first()
        if email:
            return {"message": "Email already taken"}, 422

        new_user = User(
            username=request.json.get("username"),
            email=request.json.get("email"),
            password=bcrypt.generate_password_hash(request.json.get("password")).decode('utf-8'),
            role=request.json.get("role", "user")
        )

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)
        return {"user": new_user.to_dict(), "access_token": access_token, "success": True, "message": "User has been created successfully"}, 201

class Login(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return {
                "user": user.to_dict(),
                "access_token": access_token,
                "success": True,
                "message": "Login successful"
            }, 200
        return {"message": "Invalid credentials"}, 401

class VerifyToken(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            return {
                "user": user.to_dict(),
                "success": True,
                "message": "Token is valid"
            }, 200
        return {"message": "Invalid token"}, 401

class Events(Resource):
    def get(self):
        events = Event.query.all()
        return [event.to_dict() for event in events], 200

    @jwt_required()
    def post(self):
        data = request.json
        if 'name' not in data or 'datetime' not in data or 'location' not in data:
            return {'error': 'Missing required fields'}, 400
        event = Event(image=data['image'], name=data['name'], datetime=data['datetime'], location=data['location'], capacity=data['capacity'], description=data['description'])
        db.session.add(event)
        db.session.commit()
        return event.to_dict(), 201



api.add_resource(Home, '/')
api.add_resource(Users, '/users')
api.add_resource(Login, '/login')
api.add_resource(VerifyToken, '/verify-token')
api.add_resource(Events, '/events')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
