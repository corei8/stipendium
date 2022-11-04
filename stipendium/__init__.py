from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
        UserMixin, login_user, LoginManager, login_required,
        logout_user, current_user
        )
from os import path, mkdir

basedir = path.abspath(path.dirname(__file__))


try:
    mkdir(basedir + '/databases')
except FileExistsError:
    pass

app = Flask(__name__)
# TODO: make .env file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+path.join(basedir, 'databases', 'book.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'txWufrjMigCiVQJF2TBmiA'
app.config['DEBUG'] = True

# app.config.from_object('settings.DevelopmentConfig')

db = SQLAlchemy(app)

import stipendium.views
