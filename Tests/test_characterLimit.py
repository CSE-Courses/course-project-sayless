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

def test_characterLimit():
    """Make sure Character Limit works."""

    # testing chat get
    db.create_all()

    password = ("hello123").encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())

    user = User(username="test",first_name="test",last_name="test",email="shazm@gmail.com",password=password)

    db.session.add(user)
    db.session.commit()

    client1 = app.test_client()

    # login both users to test end to end
    login("shazm@gmail.com","hello123", client1)

    # test0 : test correct character count returned
    rv = character("Hello", client1)
    assert rv.status_code == 200
    assert rv.data == b'{"Success":20,"limit":25}\n'

    # test1 : test correct character count returned
    rv = character("Hello " + list(UNICODE_EMOJI.keys())[0], client1)
    assert rv.status_code == 200
    assert rv.data == b'{"Success":20,"limit":25}\n'

    # test2 : test limit is correctly shown
    rv = character("ABCDEFGHIJ "+ list(UNICODE_EMOJI.keys())[0] +" KLMNOPQRSTUVWXYZ", client1)
    assert rv.status_code == 200
    assert rv.data == b'{"Exceeded":1,"limit":25}\n'

    db.reflect()
    db.drop_all()

# helpers for tests
def login(email, password, client):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def character(message, client):
    return client.post('/character_limit', data=message, follow_redirects=False)