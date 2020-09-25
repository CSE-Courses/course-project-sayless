import os

from flask import Flask, render_template, request, redirect

# create the flask app
app = Flask(__name__, static_url_path='', static_folder='../statics', template_folder='../templates')
app.config.from_mapping(
    SECRET_KEY='CSE'
)
app.config.from_pyfile('config.py', silent=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        # Do stuff for get request
        print("In GET")
    else:
        # Do stuff for post request
        print("In POST")

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'GET':
        # Do stuff for get request
        print("In GET")
    else:
        # Do stuff for post request
        print("In POST")

    # Should render login page but redirecting for now
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'GET':
        # Do stuff for get request
        print("In GET")
    else:
        # Do stuff for post request
        print("In POST")

    # Should render the sign up page but redirecting for now
    return redirect('/')