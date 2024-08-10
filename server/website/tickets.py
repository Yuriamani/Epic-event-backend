from flask import Blueprint, request
from .models import db, Ticket
from .utils import validate_request_data, handle_error
from flask_restful import Api, Resource

tickets = Blueprint('tickets', __name__)
api = Api(tickets)

class Tickets(Resource):
    def get(self):
        tickets = Ticket.query.all()
        return [ticket.to_dict() for ticket in tickets], 200

    def post(self):
        data = request.json
        required_fields = ['price', 'ticket_number', 'event_id']
        if not validate_request_data(data, required_fields):
            return handle_error('Missing required fields', 400)
        ticket = Ticket(price=data['price'], ticket_number=data['ticket_number'], event_id=data['event_id'])
        db.session.add(ticket)
        db.session.commit()
        return ticket.to_dict(), 201
    
    def patch(self):
        data = request.json
        id = data.get('id')
        if id is None:
            return {'error': 'Missing ticket ID'}, 400

        ticket = Ticket.query.get(id)
        if ticket is None:
            return {'error': 'ticket not found'}, 404

        if 'price' in data:
            ticket.price = data['price']
        if 'ticket_number' in data:
            ticket.ticket_number = data['ticket_number']
        if 'event_id' in data:
            ticket.event_id = data['event_id']

        db.session.commit()
        return ticket.to_dict(), 200
    
    def delete(self):
        data = request.json
        id = data.get('id')
        if id is None:
            return {'error': 'Missing ticket ID'}, 400

        ticket = Ticket.query.get(id)
        if ticket is None:
            return {'error': 'ticket not found'}, 404

        db.session.delete(ticket)
        db.session.commit()
        return {'message': 'ticket deleted successfully'}, 200

api.add_resource(Tickets, '/tickets')    