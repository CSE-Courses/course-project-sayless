import os
import bcrypt
import urllib.parse 

from flask import Flask, render_template, request, Response, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from SayLess.database import *
from SayLess.helpers import *

# create the flask app
app = Flask(__name__, static_url_path='', static_folder='../statics', template_folder='../templates')
app.config.from_mapping(
    SECRET_KEY='CSE'
)

params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=shazmaan.database.windows.net;DATABASE=sayless;UID=Shazmaan;PWD=Malek0572!")

app.config.from_pyfile('config.py', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect={}".format(params)

print(app.config['SQLALCHEMY_DATABASE_URI'])

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db.init_app(app)
db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        # Do stuff for get request
        print("In GET")
        return render_template('home.html')
    else:
        # Do stuff for post request
        print("In POST")

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'GET':
        # render login.html
        return render_template('login.html')
    else:
        # get the form_data and check with the DB if the user name or email is valid
        form_data = request.form

        if('' in form_data.keys() or '' in form_data.values()):
            return jsonify("Please fill out every field")

        email = replace(form_data.get("email"))
        password = replace(form_data.get("password"))

        if(checkViaRegex(email,'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$') == False):
            return jsonify("Invalid email")

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
                response = jsonify("Success")
                return response
            else:
                return jsonify("invalid_password")

    # return error
    return jsonify("error")

@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'GET':
        # Do stuff for get request
        return render_template("registration.html")
    else:
        # Do stuff for post request
        form_data = request.form

        if('' in form_data.keys() or '' in form_data.values()):
            return jsonify("Please fill out every field")

        email = replace(form_data.get("email"))
        username = replace(form_data.get("username"))
        confirm = replace(form_data.get("confirm"))
        password = replace(form_data.get("password"))
        
        if(checkViaRegex(email,'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$') == False):
            return jsonify("Invalid email")
       
        fname = replace(form_data.get("fname"))
        lname = replace(form_data.get("lname"))

        print("Fine until here: ")
        print(request.form)
        
        email_check = User.query.filter_by(email=email).first()
        username_check = User.query.filter_by(username=username).first()
        if len(password) < 8:
            return jsonify("password too short")
        elif username_check != None and username_check.username == username:
            return jsonify("username exists")
        elif email_check != None and email_check.email == email:
            return jsonify("email exists")
        elif password != confirm:
            return jsonify("password does not match")
        else:
            password = password.encode('utf-8')
            password = bcrypt.hashpw(password, bcrypt.gensalt())
            me = User(username=username,email=email,first_name=fname,last_name=lname,password=password)
            db.session.add(me)
            db.session.commit()

    return jsonify("success")