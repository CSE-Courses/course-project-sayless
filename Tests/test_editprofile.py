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

def test_editprofile():
    """Make sure edit profile works."""

    # testing chat get
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

    # login both users to test end to end
    login("shazm@gmail.com","hello123", client1)

    # test0 : test if edit profile page renders for client1
    rv = client1.get("/avi")
    assert rv.status_code == 200

    # test1 : test if redirected to login page for invalid sign in
    rv = client2.get("/avi")
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