from flask_sqlalchemy import SQLAlchemy
from stipendium import db
from datetime import datetime



class User(db.Model):
    """Not in use. eventualy for Logins"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Stipend(db.Model):
    """Contains all information for individual stipends"""
    __tablename__ = "stipends"
    id            = db.Column(db.Integer, primary_key=True)
    intention     = db.Column(db.String(120), unique=False, nullable=False)
    requester     = db.Column(db.String(25), unique=False, nullable=False)
    priest_asked  = db.Column(db.String(25), unique=False, nullable=False)
    origin        = db.Column(db.Integer, unique=False, nullable=False)
    accepted      = db.Column(db.DateTime, default=datetime.now)
    req_date      = db.Column(db.DateTime, nullable=True)
    amount        = db.Column(db.Integer, nullable=False)
    masses        = db.Column(db.Integer, default=1, nullable=False)
    closed        = db.Column(db.DateTime, nullable=True) # TODO: make this boolean

    def __repr__(self):
        return '<Stipend %r>' % self.id


class Closed(db.Model):
    """Closed Stipends"""
    __tablename__ = "closed"
    id            = db.Column(db.Integer, primary_key=True)
    closed        = db.Column(db.DateTime, nullable=True)
    center        = db.Column(db.String(6), unique=False, nullable=False)
    celebrant     = db.Column(db.String(25), unique=False, nullable=True)

    def __repr__(self):
        return '<Closed Stipend %r>' % self.id


class Centers(db.Model):
    """Admin mutable, holds information for exporting stipends"""
    __tablename__     = "centers"
    id                = db.Column(db.Integer, primary_key=True)
    fullname          = db.Column(db.String(35), unique=False, nullable=False)
    priests           = db.Column(db.Integer, nullable=False)
    address           = db.Column(db.String(25), unique=False, nullable=False)
    city              = db.Column(db.String(25), unique=False, nullable=False)
    state             = db.Column(db.String(25), unique=False, nullable=False)
    country           = db.Column(db.String(25), unique=False, nullable=False)
    intentions_count  = db.Column(db.Integer, nullable=False) # ?? not necessary?
    intentions_closed = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Centers %r>' % self.name

class Exports(db.Model):
    """Keeps track of all exports to ensure no overlap"""
    __tablename__ = 'exports'
    id            = db.Column(db.Integer, primary_key=True)
    exported      = db.Column(db.PickleType, nullable=False)
    center        = db.Column(db.String(6), nullable=False)
    date          = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Exports %r>' % self.id

