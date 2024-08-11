from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
import re
import datetime

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(129), nullable=False)
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.DateTime, default=db.func.now())

    @validates('email')
    def validate_email(self, key, email):
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": str(self.created_at),
        }

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    location = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Event {self.id}, {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "image": self.image,
            "name": self.name,
            "datetime": str(self.datetime),
            "location": self.location,
            "capacity": self.capacity,
            "description": self.description,
        }

class UserEvent(db.Model):
    __tablename__ = 'user_events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False, unique=True)
    ticket_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<UserEvent {self.id}, {self.user_id}, {self.event_id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_id": self.event_id,
            "ticket_number": self.ticket_number,
        }

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Feedback {self.id}, {self.user_id}, {self.event_id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_id": self.event_id,
            "feedback": self.feedback,
            "created_at": str(self.created_at),
        }

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    ticket_number = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Ticket {self.id}, {self.event_id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "ticket_number": self.ticket_number,
            "price": self.price,
        }

class EventOrganizer(db.Model):
    __tablename__ = 'event_organizers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False, unique=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    def __repr__(self):
        return f'<EventOrganizer {self.id}, {self.event_id}, {self.organizer_id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "organizer_id": self.organizer_id,
        }
