from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
# class Event(db.Model):
#     pass
# class Comment(db.Model):
#     pass
# class Order(db.Model):
#     pass