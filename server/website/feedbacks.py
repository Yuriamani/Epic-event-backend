from flask import Blueprint, request
from .models import db, Feedback
from .utils import validate_request_data, handle_error
from flask_restful import Api, Resource

feedbacks = Blueprint('feedbacks', __name__)
api = Api(feedbacks)

class Feedbacks(Resource):
    def get(self):
        feedbacks = Feedback.query.all()
        return [feedback.to_dict() for feedback in feedbacks], 200

    def post(self):
        data = request.json
        required_fields = ['feedback', 'event_id', 'user_id']
        if not validate_request_data(data, required_fields):
            return handle_error('Missing required fields', 400)
        feedback = Feedback(feedback=data['feedback'], event_id=data['event_id'], user_id=data['user_id'])
        db.session.add(feedback)
        db.session.commit()
        return feedback.to_dict(), 201
    
    def patch(self):
        data = request.json
        id = data.get('id')
        if id is None:
            return {'error': 'Missing feedback ID'}, 400

        feedback = Feedback.query.get(id)
        if feedback is None:
            return {'error': 'feedback not found'}, 404

        if 'feedback' in data:
            feedback.feedback = data['feedback']
        if 'event_id' in data:
            feedback.event_id = data['event_id']
        if 'user_id' in data:
            feedback.user_id = data['user_id']

        db.session.commit()
        return feedback.to_dict(), 200
    
    def delete(self):
        data = request.json
        id = data.get('id')
        if id is None:
            return {'error': 'Missing feedback ID'}, 400

        feedback = Feedback.query.get(id)
        if feedback is None:
            return {'error': 'feedback not found'}, 404

        db.session.delete(feedback)
        db.session.commit()
        return {'message': 'feedback deleted successfully'}, 200

api.add_resource(Feedbacks, '/feedbacks') 