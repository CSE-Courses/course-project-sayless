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

def test_login():
    """Make sure login works."""

    # testing login get
    rv = app.test_client().get("/login")
    assert rv.status_code == 200
    assert render_template("login.html").encode('utf-8') in rv.data

    # testing login post
    password = ("hello123").encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())

    db.create_all()

    user = User(username="test",first_name="test",last_name="test",email="shazm@gmail.com",password=password)

    db.session.add(user)
    db.session.commit()

    # test0 : test if valid login is made
    rv = login('shazm@gmail.com', 'hello123')
    assert rv.status_code == 200
    assert b'Success' in rv.data

    # test1 : test if email is absent
    rv = login('shazm'+ 'x' + '@gmail.com', 'hello123')
    assert rv.status_code == 200
    assert b'user_and_email_not_found' in rv.data

    # test2 : test if password is incorrect
    rv = login('shazm@gmail.com', 'hello123' + 'x')
    assert rv.status_code == 200
    assert b'invalid_password' in rv.data

    # test3 : test if frontend overriden and empty values sent
    rv = login('', 'hello123')
    assert rv.status_code == 200
    assert b'Please fill out every field' in rv.data

    # test4 : test if email is valid
    rv = login('shazm@com', 'hello123' + 'x')
    assert rv.status_code == 200
    assert b'Invalid email' in rv.data

    db.reflect()
    db.drop_all()

# helpers for tests
def login(email, password):
    return app.test_client().post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)