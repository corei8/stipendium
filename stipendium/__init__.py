from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
        UserMixin, login_user, LoginManager, login_required,
        logout_user, current_user
        )
from os import path, mkdir

# from dotenv import load_dotenv

# load_dotenv()

basedir = path.abspath(path.dirname(__file__))
ROOT = path.dirname(path.realpath(__file__))


try:
    mkdir(basedir + '/downloads')
except FileExistsError:
    pass

app = Flask(__name__)

app.config.from_prefixed_env()

db = SQLAlchemy(app)

import stipendium.views
