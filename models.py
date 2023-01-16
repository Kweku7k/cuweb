from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False,unique=False)
    phone = db.Column(db.String)
    telegramBot = db.Column(db.String)
    chatId = db.Column(db.String)
    balance = db.Column(db.String, default=0)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), primary_key=False, unique=False, nullable=False)
    def __repr__(self):
        return '<User {}>'.format(self.username)
