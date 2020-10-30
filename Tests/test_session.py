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

db.reflect()
db.drop_all()

def test_session():
    """Make sure sessions work."""
    
    db.create_all()

    password = ("hello123").encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())

    user = User(username="test",first_name="test",last_name="test",email="shazm@gmail.com",password=password)
    user2 = User(username="test2",first_name="test2",last_name="test2",email="shazm2@gmail.com",password=password)

    current_room = user2.username + user.username

    conv = Conversation(room=current_room)
    message = Message(sender=user.username, message="hello")
    message2 = Message(sender=user2.username, message="world")

    conv.message = [message, message2]

    db.session.add(user)
    db.session.add(user2)
    db.session.add(conv)
    db.session.commit()

    client1 = app.test_client()
    client2 = app.test_client()

    history = ""

    for message in conv.message:
        history += message.sender + ': ' + message.message + '\n'

    # login user
    login("shazm@gmail.com","hello123", client1)

    # test0 : test if the profile page loads if the user is logged in
    rv = client1.get("/profile")
    assert rv.status_code == 200
    assert render_template("profile.html", username=user.username, FirstName=user.first_name, LastName=user.last_name).encode('utf-8') in rv.data

    # test1 : homepage should load if user is signed in
    rv = client1.get("/homepage")
    assert rv.status_code == 200
    assert render_template("home.html").encode('utf-8') in rv.data

    # test2 : test if chat renders for client1
    rv = client1.get("/chat/" + current_room)
    assert rv.status_code == 200
    assert render_template("chat.html", messages=history, user=user.username).encode('utf-8') in rv.data

    # test3 : test if redirected to login page for invalid sign in I.e, session is missing
    rv = client2.get("/profile")
    assert rv.status_code == 302
    assert rv.location.endswith("/login")

    # test4 : test if redirected to login page for invalid sign in I.e, session is missing
    rv = client2.get("/homepage")
    assert rv.status_code == 302
    assert rv.location.endswith("/login")

    # test5 : test if redirected to login page for invalid sign in I.e, session is missing
    rv = client2.get("/chat/" + current_room)
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