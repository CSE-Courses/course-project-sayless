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

def test_search():
    """Make sure search works."""

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

    # testing search post for client1

    # test0 : test if all users are retured
    rv = search(client1)
    assert rv.status_code == 200
    assert b'["test2"]\n' in rv.data

    # test1 : test if no user is returned for request upon invalid sign in
    rv = search(client2)
    assert rv.status_code == 200
    assert b'' in rv.data

    # test2 : test if get request is made 404 is returned
    rv = client1.get("/search")
    assert rv.status_code == 404

    db.reflect()
    db.drop_all()

# helpers for tests
def login(email, password, client):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def search(client):
    return client.post('/search', follow_redirects=True)