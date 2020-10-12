
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    password = db.Column(db.String(600))

    def __repr__(self):
        return '<User %r>' % self.username

class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username1 = db.Column(db.String(200))
    username2 = db.Column(db.String(200))
    # rooms should be unique but leaving as such for testing logic
    room = db.Column(db.String(200))

class Conversation(db.Model):
    __tablename__ = 'conversation'

    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(200),unique=True)
    # rooms should be unique but leaving as such for testing logic
    message = db.relationship("Message", backref="conversation")

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    sender = db.Column(db.String(200))
    # rooms should be unique but leaving as such for testing logic
    message = db.Column(db.Text)