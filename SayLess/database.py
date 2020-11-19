
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serial

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    password = db.Column(db.String(600))
    bio = db.Column(db.String(500))

    def __repr__(self):
        return '<User %r>' % self.username

    #Our Methods for dealing with the tokens 
    #Note this one doesn't use self and thus must be given a static label
    @staticmethod
    def correct_token(token):
        s = Serial("secret_key")
        #Since loads breaks if the token is expired we throw this in a try block
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        #if we get here the token was valid and we can return the user associated with said token
        return User.query.get(user_id)

    #Simply creates a token that expires in ___ seconds, currently set at 10 minutes
    def create_token(self , seconds=600):
        s = Serial("secret_key" , seconds)
        return s.dumps({'user_id' : self.id}).decode('utf-8')

class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True,unique=True)
    username1 = db.Column(db.String(200),unique=False)
    username2 = db.Column(db.String(200),unique=False)
    new_message = db.Column(db.Boolean , default=False , nullable=False )
    # rooms should be unique but leaving as such for testing logic
    room = db.Column(db.String(300))

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
    message = db.Column(db.UnicodeText())
    mysql_charset='utf8mb4'