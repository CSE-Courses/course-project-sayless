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

def test_resetrequest():
    """Make sure reset request works."""

    # testing reset request get
    db.create_all()

    password = ("hello123").encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())

    user = User(username="test",first_name="test",last_name="test",email="shazm@gmail.com",password=password)

    db.session.add(user)
    db.session.commit()

    client1 = app.test_client()

    # login user
    login("shazm@gmail.com","hello123", client1)

    # test0 : test if request request page renders
    rv = client1.get("/reset_request")
    assert rv.status_code == 200
    
    # test1 : test if "Success" is returned as the output for valid request
    rv = reset_request(user.email, client1)
    assert b'Success' in rv.data

    db.reflect()
    db.drop_all()

# helpers for tests
def login(email, password, client):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def reset_request(email, client):
    return client.post('/reset_request', data=dict(
        email=email
    ), follow_redirects=True)