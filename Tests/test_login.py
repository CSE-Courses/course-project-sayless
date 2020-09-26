# Do NOT modify this file without consulting the team.
import os
import tempfile
import pytest
import bcrypt

# Do not remove this line. You need this to access content from the main directory
import sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from SayLess import app
from SayLess.database import *

from flask import render_template

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://shazmaan:50215152@tethys.cse.buffalo.edu:3306/shazmaan_db'
app.app_context().push()

db.init_app(app)
db.create_all()

def test_login():
    """Make sure login works."""

    # testing login get
    rv = app.test_client().get("/login")
    assert rv.status_code == 200
    assert render_template("login.html").encode('utf-8') in rv.data

    # testing login post
    password = ("hello123").encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())

    user = User(username="test",first_name="test",last_name="test",email="shazm@gmail.com",password=password)

    db.session.add(user)
    db.session.commit()

    rv = login('shazm@gmail.com', 'hello123')
    assert rv.status_code == 200
    assert b'Success' in rv.data

    rv = login('shazm@gmail.com' + 'x', 'hello123')
    assert rv.status_code == 200
    assert b'user_and_email_not_found' in rv.data

    rv = login('shazm@gmail.com', 'hello123' + 'x')
    assert rv.status_code == 200
    assert b'invalid_password' in rv.data

    db.reflect()
    db.drop_all()

# helpers for tests
def login(email, password):
    return app.test_client().post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)