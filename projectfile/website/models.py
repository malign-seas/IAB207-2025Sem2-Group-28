from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False) #128 length for hashed passwords
# class Event(db.Model):
#     pass
# class Comment(db.Model):
#     pass
# class Order(db.Model):
#     pass