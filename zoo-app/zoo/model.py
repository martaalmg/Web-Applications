from . import db
import flask_login

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    info = db.Column(db.String(512), nullable=False)
    img = db.Column(db.String(512), nullable=False)
    type = db.Column(db.String(64), nullable=False)
    zone = db.Column(db.String(64), nullable=False)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    info = db.Column(db.String(512), nullable=False)
    age = db.Column(db.String(512), nullable=False, unique=False)
    zone = db.Column(db.String(512), nullable=False, unique=False)
    featured = db.Column(db.Boolean) # if true => activity showed at the main page 
    scheduled = db.relationship("Scheduled", backref="activity", lazy=True)

class Scheduled(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    time_date = db.Column(db.DateTime(), nullable=False, unique=False)
    place = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    reservations = db.relationship("Reservation", backref="scheduled", lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('scheduled.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_time = db.Column(db.DateTime(), nullable=False, unique=False)
    places = db.Column(db.Integer, nullable=False)

class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Boolean, nullable=False)# if True => user is a costumer 
    reservations = db.relationship("Reservation", backref="user", lazy=True)
