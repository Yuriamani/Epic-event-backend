from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
import datetime

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    serialize_only = ('id', 'email', 'username')
    exclude = ('orders',)

    def __repr__(self):
        return f'<User {self.id}, {self.username}>'

class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    datetime = db.Column(db.Text, nullable=False)  # Changed from DateTime to Text
    location = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    serialize_only = ('id', 'image', 'name', 'datetime', 'location', 'capacity', 'description')
    exclude = ('user_events', 'feedback', 'tickets', 'event_organizers')

    def __repr__(self):
        return f'<Event {self.id}, {self.name}>'

class UserEvent(db.Model, SerializerMixin):
    __tablename__ = 'user_events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    ticket_number = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref=db.backref('user_events', cascade='all, delete-orphan'))
    event = db.relationship('Event', backref=db.backref('user_events', cascade='all, delete-orphan'))

    serialize_only = ('id', 'user_id', 'event_id', 'ticket_number')
    exclude = ('user', 'event')

    def __repr__(self):
        return f'<UserEvent {self.id}, {self.user_id}, {self.event_id}>'

class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    event = db.relationship('Event', backref=db.backref('feedback', cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('feedback', cascade='all, delete-orphan'))

    serialize_only = ('id', 'user_id', 'event_id', 'feedback', 'created_at')
    exclude = ('user', 'event')

    def __repr__(self):
        return f'<Feedback {self.id}, {self.user_id}, {self.event_id}>'

class Ticket(db.Model, SerializerMixin):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Added user_id to link ticket to a user
    ticket_number = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    event = db.relationship('Event', backref=db.backref('tickets', cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('tickets', cascade='all, delete-orphan'))

    serialize_only = ('id', 'event_id', 'user_id', 'ticket_number', 'price')
    exclude = ('event', 'user')

    def __repr__(self):
        return f'<Ticket {self.id}, {self.event_id}>'

class EventOrganizer(db.Model, SerializerMixin):
    __tablename__ = 'event_organizers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event = db.relationship('Event', backref=db.backref('event_organizers', cascade='all, delete-orphan'))
    organizer = db.relationship('User', backref=db.backref('event_organizers', cascade='all, delete-orphan'))

    serialize_only = ('id', 'event_id', 'organizer_id')
    exclude = ('event', 'organizer')

    def __repr__(self):
        return f'<EventOrganizer {self.id}, {self.event_id}, {self.organizer_id}>'
