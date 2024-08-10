from flask import Blueprint, request, make_response
from .models import UserEvent, EventOrganizer
from flask_restful import Api, Resource

views = Blueprint('views', __name__)
api = Api(views)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Events RESTful API",
        }
        return make_response(response_dict, 200)

class UserEvents(Resource):
    def get(self):
        user_events = UserEvent.query.all()
        return [user_event.to_dict() for user_event in user_events], 200

class EventOrganizers(Resource):
    def get(self):
        event_organizers = EventOrganizer.query.all()
        return [event_organizer.to_dict() for event_organizer in event_organizers], 200



api.add_resource(Home, '/')
api.add_resource(UserEvents, '/user_events')
api.add_resource(EventOrganizers, '/event_organizers')    