from flask_sqlalchemy import SQLAlchemy
from stipendium import db
from datetime import datetime

# db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Stipend(db.Model):
    __tablename__ = "stipends"
    id            = db.Column(db.Integer, primary_key=True)
    intention     = db.Column(db.String(120), unique=False, nullable=False)
    requester     = db.Column(db.String(25), unique=False, nullable=False)
    origin        = db.Column(db.String(6), unique=False, nullable=False)
    accepted      = db.Column(db.DateTime, default=datetime.now)
    req_date      = db.Column(db.DateTime, nullable=True)
    amount        = db.Column(db.Integer, nullable=False)
    masses        = db.Column(db.Integer, default=1, nullable=False)
    celebrant     = db.Column(db.String(25), unique=False, nullable=True)
    closed        = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Stipend %r>' % self.id
