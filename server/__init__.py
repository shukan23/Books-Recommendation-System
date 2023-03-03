from flask import Flask,flash,render_template, redirect, session, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager, login_manager, login_user, logout_user, login_required ,UserMixin)
from datetime import datetime
# from server.forms import LoginForm,RegistrationForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SECRET_KEY'] = 'shukanS'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_one'
login_manager.login_message_category = 'info'

# with app.app_context():
#     db.create_all()

from server import routes
