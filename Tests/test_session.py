# Do NOT modify this file without consulting the team.
import os
import pytest
import bcrypt
import json

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

def test_session():
    """Make sure sessions work."""
    
    db.create_all()

    password = ("hello123").encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())

    user = User(username="test",first_name="test",last_name="test",email="shazm@gmail.com",password=password)
    user2 = User(username="test2",first_name="test2",last_name="test2",email="shazm2@gmail.com",password=password)

    db.session.add(user)
    db.session.add(user2)
    db.session.commit()

    client1 = app.test_client()
    client2 = app.test_client()

    # login user
    login("shazm@gmail.com","hello123", client1)

    user2_room = json.loads(homepage(user2.username, client1).data)["Success"]

    current_room = user2_room

    # test0 : test if the profile page loads if the user is logged in
    rv = client1.get("/profile")
    assert rv.status_code == 200

    # test1 : homepage should load if user is signed in
    rv = client1.get("/homepage")
    assert rv.status_code == 200

    # test2 : test if chat renders for client1
    rv = client1.get("/chat/" + current_room)
    assert rv.status_code == 200

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

def homepage(username, client):
    return client.post('/homepage', data=dict(
        username=username
    ), follow_redirects=True)