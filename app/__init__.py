from datetime import timedelta

from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

import mysql.connector

app = Flask(__name__)
database_url = 'mysql+mysqlconnector://root@127.0.0.1:3306/teste'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = ',1(l:a_tvul~u<+~uqo6u5$9wf^q#(0;}om?b%!8.?pxo-<n%13ine&i&*89-?|'
app.config['SESSION_FILE_DIR'] = 'app/security/session'

app.permanent_session_lifetime = timedelta(days=10)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
scheduler = APScheduler()

Session(app)

app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'
app.jinja_env.block_start_string = '[%'
app.jinja_env.block_end_string = '%]'
app.jinja_env.comment_start_string = '[#'
app.jinja_env.comment_end_string = '#]'


from app.controllers import routes
