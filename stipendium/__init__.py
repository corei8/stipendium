from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
        UserMixin, login_user, LoginManager, login_required,
        logout_user, current_user
        )
from os import path, mkdir, listdir

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

# database_path = "./stipendium/databases"
# if len(listdir(database_path)) == 0: # there is no database
    # db.create_all()
    # make a fake user for login
    # hashed_pwd = generate_password_hash("iamadmin", "sha256")
    # admin_user = User(
            # name = 'temp admin',
            # username = 'admin',
            # password_hash = hashed_pwd,
            # )
    # db.session.add(new_user)
    # db.session.commit()

import stipendium.views
