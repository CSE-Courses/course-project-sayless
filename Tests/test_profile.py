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

def test_profile():
    """Make sure profile page works."""

    # testing profile get
    db.create_all()

    password = ("hello123").encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())

    user = User(username="test",first_name="test",last_name="test",email="shazm@gmail.com",password=password)

    db.session.add(user)
    db.session.commit()

    client1 = app.test_client()
    client2 = app.test_client()

    # login user
    login("shazm@gmail.com","hello123", client1)

    # test0 : test if the profile page loads
    rv = client1.get("/profile")
    assert rv.status_code == 200

    # test1 : test if redirected to login page for invalid sign in
    rv = client2.get("/profile")
    assert rv.status_code == 302
    assert rv.location.endswith("/login")

    # test2 : update Username, Lastname, Password, Username and Bio
    rv = profile("nShaz","mShaz", "hello1234", "username new", "New bio", client1)
    assert b'First Name, Last Name, Password, Username, Bio' in rv.data

    # test3 : update nothing should return that nothing has been updates
    rv = profile("", "", "", "", "", client1)
    assert b'Nothing Updated' in rv.data

    db.reflect()
    db.drop_all()

# helpers for tests
def login(email, password, client):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def profile(firstname, lastname, password, username, bio, client):
    return client.post('/profile', data=dict(
        firstname=firstname,
        lastname=lastname,
        username=username,
        bio=bio,
        password=password
    ), follow_redirects=True)