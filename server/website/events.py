from flask import Blueprint, request, jsonify
from . import db
from .models import Event
from .utils import validate_request_data, handle_error
from flask_restful import Api, Resource
from flask_login import login_required, current_user

events = Blueprint('events', __name__)
api = Api(events) 

class Events(Resource):
    def get(self):
        events = Event.query.all()
        return [event.to_dict() for event in events], 200
    
    @login_required
    def patch(self):
        if current_user.role != 'admin':
            return jsonify({'message': 'Access forbidden'}), 403
        data = request.json
        id = data.get('id')
        if id is None:
            return {'error': 'Missing event ID'}, 400

        event = Event.query.get(id)
        if event is None:
            return {'error': 'Event not found'}, 404

        if 'name' in data:
            event.name = data['name']
        if 'image' in data:
            event.image = data['image']
        if 'datetime' in data:
            event.datetime = data['datetime']
        if 'location' in data:
            event.location = data['location']
        if 'description' in data:
            event.description = data['description']
        if 'capacity' in data:
            event.capacity = data['capacity']

        db.session.commit()
        return event.to_dict(), 200

    @login_required
    def post(self):
        if current_user.role != 'admin':
            return jsonify({'message': 'Access forbidden'}), 403
        data = request.json
        required_fields = ['name', 'image', 'datetime', 'location', 'capacity', 'description']
        if not validate_request_data(data, required_fields):
            return handle_error('Missing required fields', 400)
        event = Event(name=data['name'],image=data['image'], datetime=data['datetime'], location=data['location'], capacity=data['capacity'], description=data['description'])
        db.session.add(event)
        db.session.commit()
        return event.to_dict(), 201
    
    
class EventResource(Resource):
    def get(self, id):
        if id is None:
            return {'error': 'Missing event ID'}, 400

        event = Event.query.get(id)
        if event is None:
            return {'error': 'Event not found'}, 404
        return event.to_dict(), 200

    @login_required
    def delete(self, id):
        if current_user.role != 'admin':
            return jsonify({'message': 'Access forbidden'}), 403
        if id is None:
            return {'error': 'Missing event ID'}, 400

        event = Event.query.get(id)
        if event is None:
            return {'error': 'Event not found'}, 404

        db.session.delete(event)
        db.session.commit()
        return {'message': 'Event deleted successfully'}, 204   

api.add_resource(EventResource, "/events/<int:id>")
api.add_resource(Events, "/events")