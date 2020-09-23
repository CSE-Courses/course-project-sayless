import os
import bcrypt

from flask import Flask, render_template, request, Response, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from SayLess.database import *
from SayLess.helpers import *

# create the flask app
app = Flask(__name__, static_url_path='', static_folder='../statics', template_folder='../templates')
app.config.from_mapping(
    SECRET_KEY='CSE'
)
app.config.from_pyfile('config.py', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://moulidah:50223020@tethys.cse.buffalo.edu:3306/moulidah_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db.init_app(app)
db.create_all()
# me = User('admin', 'admin@example.com')
# db.session.add(me)
# db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        # Do stuff for get request
        print("In GET")
        return redirect('/login')
    else:
        # Do stuff for post request
        print("In POST")

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'GET':
        # render login.html
        return render_template('dummy.html')
    else:
        # get the form_data and check with the DB if the user name or email is valid
        form_data = request.form

        email = replace(form_data.get("email"))
        password = replace(form_data.get("password"))

        password = password.encode('utf-8')

        # verify if the user is present
        check_email = User.query.filter_by(email=email).first()

        if(check_email is None):
            return jsonify("user_and_email_not_found")
        else:
            # if user is present check if the password is correct
            stored_password = None

            stored_password = check_email.password

            stored_password = stored_password.encode('utf-8')

            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            if bcrypt.checkpw(password, stored_password):
                response = make_response(jsonify("Success"))
                return response
            else:
                return jsonify("invalid_password")

    # return error
    return jsonify("error")

@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'GET':
        # Do stuff for get request
        return render_template("dummy2.html")
    else:
        # Do stuff for post request
        form_data = request.form
        email = form_data.get("email")
        print(type(email))
        password = form_data.get("password")
        password = password.encode('utf-8')
        fname = form_data.get("fname")
        lname = form_data.get("lname")

        me = User(email,email,fname,lname,password)
        db.session.add(me)
        db.commit()
        return render_template("home.html")

    # Should render the sign up page but redirecting for now
    return "failed"

