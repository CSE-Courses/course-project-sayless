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

def test_registration():
    """Make sure registration works."""

    # testing registration get
    rv = app.test_client().get("/signup")
    assert rv.status_code == 200
    assert render_template("registration.html").encode('utf-8') in rv.data

    # testing registration post    
    db.create_all()

    # test0 : verify if backend returns "fill out every field" if missing field
    rv = register('','shazm@gmail.com','','test','hello123','hello123')
    assert rv.status_code == 200
    assert b'Please fill out every field' in rv.data

    # test1 : verify a valid input
    rv = register('test','shazm@gmail.com','test','test','hello123','hello123')
    user = User.query.filter(User.email=="shazm@gmail.com",User.username=="test",User.first_name=="test",User.last_name=="test").first()
    password = ("hello123").encode('utf-8')
    stored_password = user.password.encode('utf-8')

    assert rv.status_code == 200
    assert b'success' in rv.data
    # check if user can be found
    assert user != None
    # check if the password stored is the same as inserted password
    assert bcrypt.checkpw(password, stored_password)

    # test2 : verify if backend recognizes a shorter password
    rv = register('test2','shazm2@gmail.com','test2','test2','hello13','hello13')
    assert rv.status_code == 200
    assert b'password too short' in rv.data

    # test3 : verify if backend recognizes a existing username
    rv = register('test','shazm3@gmail.com','test3','test3','hello123','hello123')
    assert rv.status_code == 200
    assert b'username exists' in rv.data

    # test4 : verify if backend recognizes a existing email
    rv = register('test4','shazm@gmail.com','test4','test4','hello123','hello123')
    assert rv.status_code == 200
    assert b'email exists' in rv.data

    # test5 : verify if backend recognizes if the passwords don't match
    rv = register('test5','shazm5@gmail.com','test5','test5','hello123','hello1234')
    assert rv.status_code == 200
    assert b'password does not match' in rv.data

    # test6 : verify if database recognizes invalid email
    rv = register('test5','shazm5.com','test5','test5','hello123','hello1234')
    assert rv.status_code == 200
    assert b'Invalid email' in rv.data

    db.reflect()
    db.drop_all()

# helpers for tests
def register(username, email, first_name, last_name, password, confirm):
    return app.test_client().post('/signup', data=dict(
        username=username,
        fname=first_name,
        lname=last_name,
        email=email,
        password=password,
        confirm=confirm
    ), follow_redirects=True)