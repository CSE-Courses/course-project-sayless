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

def test_homepage():
    """Make sure homepage works."""

    # testing homepage get
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
    client3 = app.test_client()

    # login both users to test end to end
    login("shazm@gmail.com","hello123", client1)
    login("shazm2@gmail.com","hello123", client2)

    # test7 : test if homepage renders
    rv = client1.get("/homepage")
    assert rv.status_code == 200

    # testing homepage post for client1

    # test0 : test if valid chat room was created
    rv = homepage('test2', client1)
    assert rv.status_code == 200
    assert b'Success' in rv.data

    # test1 : test if the user is trying to talk to themself
    rv = homepage('test', client1)
    assert rv.status_code == 200
    assert b'Cannot_Talk' in rv.data

    # test2 : test if the user is not present
    rv = homepage('test_not_existing', client1)
    assert rv.status_code == 200
    assert b'Invalid_user' in rv.data

    #-----

    rv = client2.get("/homepage")
    assert rv.status_code == 200

    # testing homepage post for client2

    # test3 : test if valid chat room was created
    rv = homepage('test', client2)
    assert rv.status_code == 200
    assert b'Success' in rv.data

    # test4 : test if the user is trying to talk to themself
    rv = homepage('test2', client2)
    assert rv.status_code == 200
    assert b'Cannot_Talk' in rv.data

    # test5 : test if the user doesnot exist
    rv = homepage('test_not_existing', client2)
    assert rv.status_code == 200
    assert b'Invalid_user' in rv.data


    # test6 : test if redirected to login page for invalid sign in
    rv = client3.get("/homepage")
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