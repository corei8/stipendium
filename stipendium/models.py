from flask_sqlalchemy import SQLAlchemy
from stipendium import db
from datetime import datetime



class User(db.Model):
    """User Login"""
    __tablename__ = "login"
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password      = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Queue(db.Model):
    """Contains all information for individual stipends"""
    __tablename__ = "stipends"
    id            = db.Column(db.Integer, primary_key=True)
    intention     = db.Column(db.String(120), unique=False, nullable=False)
    requester     = db.Column(db.String(25), unique=False, nullable=False)
    priest        = db.Column(db.String(25), unique=False, nullable=False)
    origin        = db.Column(db.Integer, unique=False, nullable=False)
    accepted      = db.Column(db.DateTime, default=datetime.now)
    req_date      = db.Column(db.DateTime, nullable=True)
    amount        = db.Column(db.Integer, nullable=False)
    masses        = db.Column(db.Integer, default=1, nullable=False)

    def __repr__(self):
        return '<Stipend %r>' % self.id


class Priests(db.Model):
    """Information for each of the priests."""
    __tablename__ = "priests"
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(35), unique=False, nullable=False)
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


class Centers(db.Model):
    """Admin mutable, holds information for exporting stipends"""
    __tablename__ = "centers"
    id            = db.Column(db.Integer, primary_key=True)
    fullname      = db.Column(db.String(35), unique=False, nullable=False)
    address       = db.Column(db.String(25), unique=False, nullable=False)
    city          = db.Column(db.String(25), unique=False, nullable=False)
    state         = db.Column(db.String(25), unique=False, nullable=False)
    country       = db.Column(db.String(25), unique=False, nullable=False)

    def __repr__(self):
        return '<Centers %r>' % self.fullname


class Trash(db.Model):
    """Trash bin for deleted Masses. Keep them for 30 days"""
    __tablename__ = "trash"
    id            = db.Column(db.Integer, primary_key=True)
    stipend_id    = db.Column(db.Integer)
    intention     = db.Column(db.String(120), unique=False, nullable=False)
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


