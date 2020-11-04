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
from flask_minify import minify

app.config['SQLALCHEMY_DATABASE_URI'] = get_secret("TestDB")
app.app_context().push()
app.testing = True

db.reflect()
db.drop_all()

def test_logout():
    """Make sure logout works."""

    password = ("hello123").encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())

    db.create_all()

    user = User(username="test",first_name="test",last_name="test",email="shazm@gmail.com",password=password)

    db.session.add(user)
    db.session.commit()

    client1 = app.test_client()

    # login both users to test end to end
    login("shazm@gmail.com","hello123", client1)
   
    # test0: Make sure logout is redirected to login page
    rv = client1.get("/logout")
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