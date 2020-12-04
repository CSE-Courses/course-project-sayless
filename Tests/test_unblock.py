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

def test_unblock():
    """Make sure unblock works."""

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
    login("shazm2@gmail.com","hello123", client2)

    # test0 : test if user1 can block user2
    rv = block(user2.username, client1)
    assert rv.status_code == 200
    assert rv.data == b'"Success"\n'
    assert User.query.filter_by(username=user.username).first().blocked[0].blocked_user == user2.username

    # test1 : test if user2 can block user1
    rv = block(user.username, client2)
    assert rv.status_code == 200
    assert rv.data == b'"Success"\n'
    assert User.query.filter_by(username=user2.username).first().blocked[0].blocked_user == user.username
    
    # test2 : unblock user2 for user1
    rv = unblock(user2.username, client1)
    assert rv.status_code == 200
    assert rv.data == b'"Success"\n'
    assert len(User.query.filter_by(username=user.username).first().blocked) == 0

    # test3 : unblock unblocked user for user1
    rv = unblock("Should Not work", client1)
    assert rv.status_code == 200
    assert rv.data == b'"Fail"\n'

    # test4 : unblock user1 for user2
    rv = unblock(user.username, client2)
    assert rv.status_code == 200
    assert rv.data == b'"Success"\n'
    assert len(User.query.filter_by(username=user2.username).first().blocked) == 0

    # test5 : unblock unblocked user for user1
    rv = unblock("Should Not work", client2)
    assert rv.status_code == 200
    assert rv.data == b'"Fail"\n'

    db.reflect()
    db.drop_all()

# helpers for tests
def login(email, password, client):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def block(toBlock, client):
    return client.post('/block', data=dict(
        username=toBlock,
    ), follow_redirects=True)

def unblock(toUnBlock, client):
    return client.post('/unblock', data=dict(
        username=toUnBlock,
    ), follow_redirects=True)