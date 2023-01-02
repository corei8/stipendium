# from flask_sqlalchemy import SQLAlchemy
from stipendium import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    """User Login"""
    __tablename__ = "login"
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(20), unique=True, nullable=False)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=True, nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Queue(db.Model):
    """Contains all information for individual stipends"""
    __tablename__ = "stipends"
    id            = db.Column(db.Integer, primary_key=True)
    intention     = db.Column(db.String(120), unique=False, nullable=False)
    dead          = db.Column(db.Boolean, nullable=False)
    requester     = db.Column(db.String(25), unique=False, nullable=False)
    priest        = db.Column(db.String(25), unique=False, nullable=True)
    origin        = db.Column(db.Integer, unique=False, nullable=False)
    accepted      = db.Column(db.DateTime, default=datetime.now)
    req_date      = db.Column(db.DateTime, nullable=True)
    amount        = db.Column(db.Integer, nullable=False)
    masses        = db.Column(db.Integer, default=1, nullable=False)

    def __repr__(self):
        return '<Stipend %r>' % self.id


class Center(db.Model):
    """Information for Mass Center"""
    __tablename__ = "center"
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(35), unique=False, nullable=False)
    address       = db.Column(db.String(50), unique=False, nullable=False)
    city          = db.Column(db.String(25), unique=False, nullable=False)
    state         = db.Column(db.String(25), unique=False, nullable=False)
    country       = db.Column(db.String(25), unique=False, nullable=False)

    def __repr__(self):
        return '<Centers %r>' % self.name


class Priest(db.Model):
    """Information for each of the priests."""
    __tablename__ = "priests"
    id            = db.Column(db.Integer, primary_key=True)
    firstname     = db.Column(db.String(15), unique=False, nullable=False)
    lastname      = db.Column(db.String(35), unique=False, nullable=False)
    rank          = db.Column(db.String(3), unique=False, nullable=False)
    center        = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Priests %r>' % self.name


class Exports(db.Model):
    """Keeps track of all exports to ensure no overlap"""
    __tablename__ = 'exports'
    id            = db.Column(db.Integer, primary_key=True)
    stipend       = db.Column(db.Integer, nullable=False)
    priest        = db.Column(db.Integer, nullable=False)
    center        = db.Column(db.Integer, nullable=False)
    export_date   = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Exports %r>' % self.id


class Closed(db.Model):
    """Closed Stipends, includes export date, center and priest"""
    __tablename__ = "closed"
    id            = db.Column(db.Integer, primary_key=True)
    stipend       = db.Column(db.Integer, nullable=True)
    priest        = db.Column(db.Integer, unique=False, nullable=True)
    center        = db.Column(db.Integer, unique=False, nullable=False)
    export_date   = db.Column(db.DateTime, nullable=False)
    closed_date   = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Closed Stipend %r>' % self.id


class Trash(db.Model):
    """Trash bin for deleted Masses. Keep them for 30 days"""
    __tablename__ = "trash"
    id            = db.Column(db.Integer, primary_key=True)
    stipend_id    = db.Column(db.Integer)
    intention     = db.Column(db.String(120), unique=False, nullable=False)
    dead          = db.Column(db.Boolean, default=True, nullable=True)
    requester     = db.Column(db.String(25), unique=False, nullable=False)
    priest_asked  = db.Column(db.String(25), unique=False, nullable=False)
    origin        = db.Column(db.Integer, unique=False, nullable=False)
    accepted      = db.Column(db.DateTime, nullable=False)
    req_date      = db.Column(db.DateTime, nullable=True)
    amount        = db.Column(db.Integer, nullable=False)
    masses        = db.Column(db.Integer, default=1, nullable=False)
    trashed       = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return '<Trash %r>' % self.id


class Activity(db.Model):
    """Log user activity"""
    __tablename__ = "activity"
    id            = db.Column(db.Integer, primary_key=True)
    access_date   = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
