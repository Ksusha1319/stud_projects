from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class Nickname(db.Model):
    __tablename__ = "nicknames"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return "{}".format(self.name)

class Report(db.Model):
    """"""
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000),nullable=True,)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    incident_date = db.Column(db.String(100))
    incident_type = db.Column(db.String(100),nullable=False,)
    game_type = db.Column(db.String(100),nullable=False,)
    priority = db.Column(db.String(100),nullable=False,)
    status = db.Column(db.String(100), default="NEW")
    resolution = db.Column(db.String(100), nullable=True,)
    comment_soc = db.Column(db.String(1000), nullable=True,)
    service_login = db.Column(db.String(100),nullable=False,)
    username = db.Column(db.String(100),nullable=False,)
    ticket = db.Column(db.String(100),nullable=True,)

    nickname_id = db.Column(db.Integer, db.ForeignKey("nicknames.id"))
    nickname = db.relationship("Nickname", backref=db.backref(
        "reports", order_by=id), lazy=True)
    
class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer(), primary_key=True)
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    pass_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), default="user" )
    about = db.Column(db.String(100))
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
