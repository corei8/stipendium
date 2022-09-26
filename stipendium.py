import os
from flask import (
        Flask, request, render_template, url_for, flash, redirect
        )
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms import (
        Form, BooleanField, StringField,
        PasswordField, SelectField, 
        DateTimeField, DecimalField, 
        IntegerField, validators 
        )
from wtforms.widgets import CheckboxInput, DateTimeLocalInput
# from wtforms.fields import DateTimeLocalInput

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'book.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'txWufrjMigCiVQJF2TBmiA'
db = SQLAlchemy(app)


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
    request_date  = db.Column(db.Boolean, default=False, nullable=False)
    start         = db.Column(db.DateTime, nullable=True)
    finish        = db.Column(db.DateTime, nullable=True)
    amount        = db.Column(db.Integer, nullable=False)
    masses        = db.Column(db.Integer, default=1, nullable=False)
    celebrant     = db.Column(db.String(25), unique=False, nullable=True)
    closed        = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Stipend %r>' % self.id


class StipendForm(Form):
    intention    = StringField('Intention', [validators.Length(min=5, max=120)])
    requester    = StringField('From', [validators.Length(min=5, max=25)])
    origin       = SelectField('Origin', choices=[('SLHFLA', 'Spring Lake, Florida')])
    request_date = StringField('Is there a requested date?', widget=CheckboxInput(), default=False)
    start        = StringField('Date requested', widget=DateTimeLocalInput())
    amount       = IntegerField('Stipend') 
    masses       = IntegerField('How many Masses?')


@app.route('/', methods=['POST', 'GET'])
def add_stipend():
    form = StipendForm(request.form)
    if request.method == 'POST' and form.validate():
        stipend = Stipend(
                        intention    = form.intention.data,
                        requester    = form.requester.data,
                        origin       = form.origin.data,
                        accepted     = datetime.today(),
                        request_date = form.request_date.data,
                        # start        = form.start.data,
                        # finish       = form.start.data,
                        start        = None,
                        finish       = None,
                        amount       = form.amount.data,
                        masses       = form.masses.data,
                        celebrant    = '',
                        closed       = None, # because we never add and close at the same time
                )
        db.session.add(stipend)
        db.session.commit()
        flash('Stipend added.')
        return redirect(url_for('add_stipend'))
    return render_template('add_stipend.html', form=form)

@app.route('/stipends', methods=['GET'])
def stipends():
    stipends = Stipend.query.all()
    return render_template('stipends.html', stipends=stipends)


if __name__=='__main__':
    app.debug=True
    app.run()

