from app import db
from models import User, Event, UserEvent, Feedback, Ticket, EventOrganizer

def seed_data():
    db.drop_all()
    db.create_all()

    
    user1 = User(
        username="derrick_roz",
        email="derrick@example.com",
        password_hash="hashed_password_1", 
        role="user"
    )
    user2 = User(
        username="Levis_dexta",
        email="levis@example.com",
        password_hash="hashed_password_2",
        role="organizer"
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    
    event1 = Event(
        image="https://example.com/image1.jpg",
        name="Music Concert",
        datetime="2024-09-01 19:00:00",
        location="New York City",
        capacity=5000,
        description="A grand music concert featuring top artists."
    )
    event2 = Event(
        image="https://example.com/image2.jpg",
        name="Tech Conference",
        datetime="2024-10-15 09:00:00",
        location="San Francisco",
        capacity=2000,
        description="A conference for tech enthusiasts and professionals."
    )

    db.session.add(event1)
    db.session.add(event2)
    db.session.commit()

   
    user_event1 = UserEvent(
        user_id=user1.id,
        event_id=event1.id,
        ticket_number=1234
    )
    user_event2 = UserEvent(
        user_id=user2.id,
        event_id=event2.id,
        ticket_number=5678
    )

    db.session.add(user_event1)
    db.session.add(user_event2)
    db.session.commit()

    
    feedback1 = Feedback(
        user_id=user1.id,
        event_id=event1.id,
        feedback="Amazing concert! Loved every moment."
    )
    feedback2 = Feedback(
        user_id=user2.id,
        event_id=event2.id,
        feedback="Very informative conference with great networking opportunities."
    )

    db.session.add(feedback1)
    db.session.add(feedback2)
    db.session.commit()

   
    ticket1 = Ticket(
        event_id=event1.id,
        ticket_number=1234,
        price=99.99
    )
    ticket2 = Ticket(
        event_id=event2.id,
        ticket_number=5678,
        price=199.99
    )

    db.session.add(ticket1)
    db.session.add(ticket2)
    db.session.commit()

  
    event_organizer1 = EventOrganizer(
        event_id=event1.id,
        organizer_id=user2.id
    )
    event_organizer2 = EventOrganizer(
        event_id=event2.id,
        organizer_id=user2.id
    )

    db.session.add(event_organizer1)
    db.session.add(event_organizer2)
    db.session.commit()

    print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
