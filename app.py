# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fd[pfdpdgpfgpd[gpfd[g'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = "flask rocks!"
db.init_app(app)
login = LoginManager(app)
login.login_view = 'login'

