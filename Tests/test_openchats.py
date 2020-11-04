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

def test_openchats():
    """Make sure openchats works."""

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

    user2_room = json.loads(homepage(user2.username, client1).data)["Success"]
    user_room = json.loads(homepage(user.username, client2).data)["Success"]

    # Verify both rooms are same
    assert user2_room == user_room

    current_room = user2_room

    conv = Conversation.query.filter_by(room=current_room).first()
    message = Message(sender=user.username, message="hello")
    message2 = Message(sender=user2.username, message="world")

    conv.message = [message, message2]

    db.session.add(conv)
    db.session.commit()

    # test0 : test if openchats gives correct users for client1
    rv = client1.post("/openchats")
    assert rv.status_code == 200
    assert user2.username in json.loads(rv.data.decode('utf-8'))
    assert current_room == json.loads(rv.data.decode('utf-8'))[user2.username]

    # test1 : test if openchats gives correct users for client2
    rv = client2.post("/openchats")
    assert rv.status_code == 200
    assert user.username in json.loads(rv.data.decode('utf-8'))
    assert current_room == json.loads(rv.data.decode('utf-8'))[user.username]

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
    ), follow_redirects=False)