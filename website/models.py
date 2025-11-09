from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    fullname = db.Column(db.String(100), index=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False) #128 length for hashed passwords
    phone = db.Column(db.String(10), nullable=False) #  unique=True, index=True - probably dont need a uniquness constraint on phone? if unique then indexing would be useful
    streetaddress = db.Column(db.String(255), nullable=False)
    
    bookings = db.relationship('Booking', backref='user')
    comments = db.relationship('Comment', backref='user')

    def set_password(self, raw_password, hasher):
        self.password = hasher(raw_password)
    
    def check_password(self, raw_password, checker):
        return checker(self.password, raw_password)

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Booking user_id={self.user_id}, event_id={self.event_id}>"

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    def __repr__(self):
        return f"<Comment user_id={self.user_id}, event_id={self.event_id}>"

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open')
    image = db.Column(db.String(400))
    venue = db.Column(db.String(80), nullable=False)
    tickets_left = db.Column(db.Integer, nullable=False)

    organiser_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    organiser = db.relationship('User', backref='events')

    comments = db.relationship('Comment', backref='event')

    def __repr__(self):
        return f"<Event title={self.title}, id={self.id}>"
    
    