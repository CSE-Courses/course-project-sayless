# Do NOT modify this file without consulting the team.
import os
import pytest
import bcrypt

# Do not remove this line. You need this to access content from the main directory
import sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from SayLess import app
from SayLess.database import *
from SayLess.helpers import *

from flask import render_template

app.config['SQLALCHEMY_DATABASE_URI'] = get_secret("TestDB")
app.app_context().push()

app.testing = True

db.reflect()
db.drop_all()

def test_deleteacc():
    """Make sure Delete Account page works."""

    # testing profile get
    db.create_all()

    password = ("hello123").encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())

    user = User(username="test",first_name="test",last_name="test",email="shazm@gmail.com",password=password)
    room1 = Rooms(username1="You Do Not Exist", username2=user.username, new_message=False, room="TestingRoom")
    room2 = Rooms(username1=user.username, username2="You Do Not Exist", new_message=False, room="TestingRoom")
    profile = Profile(email=user.email, filename="wut.jpeg")
    conv = Conversation(room=room1.room)
    message = Message(sender=user.username, message="you are a test")
    conv.message = [message]

    db.session.add(user)
    db.session.commit()
    db.session.add(room1)
    db.session.commit()
    db.session.add(room2)
    db.session.commit()
    db.session.add(profile)
    db.session.commit()
    db.session.add(conv)
    db.session.commit()

    client1 = app.test_client()
    client2 = app.test_client()

    # login user
    login("shazm@gmail.com","hello123", client1)

    # test0 : test if the profile page loads
    rv = delete(client1)
    assert rv.status_code == 200
    assert rv.data == b'"success"\n'
    assert User.query.filter_by(username=user.username).first() is None
    assert Profile.query.filter_by(email=user.email).first() is None
    assert Rooms.query.filter_by(username1=user.username).first() is None
    assert Rooms.query.filter_by(username2=user.username).first() is None
    assert Rooms.query.filter_by(room=room1.room).first() is None
    assert Conversation.query.filter_by(room=room1.room).first() is None
    assert Message.query.filter_by(sender=user.username).first() is None

    # test1 : test if redirected to login page for invalid sign in
    rv = client2.get("/deleteacc")
    assert rv.status_code == 302
    assert rv.location.endswith("/login")

    db.reflect()
    db.drop_all()

# helpers for tests
def login(email, password, client):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def delete(client):
    return client.post('/deleteacc', data=dict(), follow_redirects=True)