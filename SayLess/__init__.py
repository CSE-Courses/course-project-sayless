import os
import bcrypt
import urllib.parse 

from flask import Flask, render_template, request, Response, redirect, jsonify, session, make_response
from flask_socketio import SocketIO, leave_room, join_room, send, emit
from flask_sqlalchemy import SQLAlchemy
from SayLess.database import *
from SayLess.helpers import *
from datetime import timedelta

# create the flask app
app = Flask(__name__, static_url_path='', static_folder='../statics', template_folder='../templates')
app.config.from_mapping(
    SECRET_KEY='CSE'
)

params = urllib.parse.quote_plus(get_secret("DB"))

app.config.from_pyfile('config.py', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect={}".format(params)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db.init_app(app)
db.create_all()

socketio = SocketIO(app)

serverRestarted = True

@app.route('/', methods=['GET', 'POST'])
def home():
    global serverRestarted

    if(serverRestarted):
        session.clear()
        serverRestarted = False
        return redirect("/login")

    if request.method == 'GET' and 'email' in session:
        # Do stuff for get request
        print("In GET")
        return render_template('home.html')
    elif request.method == 'GET' and 'email' not in session:
        print("Invalid Login")
        return redirect("/login")
    else:
        # Do stuff for post request
        print("In POST")

    return redirect('/signup')

@app.route('/search', methods=['POST'])
def search():
    global serverRestarted

    if(serverRestarted):
        session.clear()
        serverRestarted = False
        return redirect("/login")

    if('email' in session):
        users = []

        all = db.session.query(User).all()

        for user in all:
            if user.email != session['email']:
                users.append(user.username)

        return jsonify(users)
    elif('email' not in session):
        return redirect("/login")

@app.route('/profile', methods=['GET','POST'])
def profile():
    global serverRestarted

    if(serverRestarted):
        session.clear()
        serverRestarted = False
        return redirect("/login")

    if request.method == 'GET' and 'email' in session:
        # Do stuff for get request
        print("In GET")

        # Get username, first name and last name
        username = "username"
        first_name = "First Name"
        last_name = "Last Name"

        email = User.query.filter_by(email=session['email']).first()
        if(email):
            username = email.username
            first_name = email.first_name
            last_name = email.last_name

        return render_template('profile.html', username=username, FirstName=first_name, LastName=last_name)
    elif request.method == 'GET' and 'email' not in session:
        print("Invalid access")
        return redirect("/login")
    else:

        # In Post request
        print("In POST")


@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    global serverRestarted

    if(serverRestarted):
        session.clear()
        serverRestarted = False
        return redirect("/login")

    if request.method == 'GET' and 'email' in session:
        # Do stuff for get request
        print("In GET")

        return render_template('home.html')
    elif request.method == 'GET' and 'email' not in session:
        print("Invalid access")
        return redirect("/login")
    else:
        # Do stuff for post request

        print("In POST")

        form_data = request.form

        username = replace(form_data.get("username"))

        # this whole step is checking if a username exist or if you have already created a chat with a user
        username_check = User.query.filter_by(username=username).first()

        # check if the person is trying to talk to themselves
        email = session['email']
        email_check = User.query.filter_by(email=email).first()
        if(email_check.username == username):
            return jsonify({'Cannot_Talk':username})

        if username_check is None:
            return jsonify({'Invalid_user':"invalid"})

        session['username2'] = username
        username_check1 = Rooms.query.filter_by(username1=username,username2=session['username']).first()
        username_check2 = Rooms.query.filter_by(username1=session['username'],username2=username).first()

        currentroom = "DUMMY"

        # this is checking if the user already has a room created with this searach user.
        if username_check1 is None and username_check2 is None:
            currentroom = username + session['username']
            me = Rooms(username1 = session['username'], username2 = username, room = currentroom )
            me2 = Rooms(username1 = username, username2 = session['username'], room = currentroom )
            db.session.add(me)
            db.session.add(me2)
            db.session.commit()
        else:
            # if the search user is username1 then we enter here
            currentroom = username_check2.room

        resp = make_response(jsonify({'Success':currentroom}))

        conversation = Conversation.query.filter_by(room=currentroom).first()
        if(conversation is None and currentroom != "DUMMY"):
            conversation = Conversation(room = currentroom)
            db.session.add(conversation)
            db.session.commit()
        
        return resp

    return redirect('home.html')

@app.route('/chat/<string:room_number>', methods=['GET', 'POST'])
def chat(room_number):
    global serverRestarted

    if(serverRestarted):
        session.clear()
        serverRestarted = False
        return redirect("/login")

    # verify if the current user is allowed to access the room

    if request.method == 'GET' and 'email' in session:
        # Do stuff for get request
        print("Rendering chat template")

        email_check = User.query.filter_by(email=session['email']).first()

        history = ""

        # check history of messages and load all of them
        conversation = Conversation.query.filter_by(room = room_number).first()
        if(conversation):
            messages = conversation.message

            for message in messages:
                history += message.sender + ': ' + message.message + '\n'

        return render_template('chat.html', messages=history, user=email_check.username)
    elif request.method == 'GET' and 'email' not in session:
        print("Invalid access")
        return redirect("/login")
    else:
        # Do stuff for post request
         print("In POST")


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
                session['email'] = email
                session['username'] = check_email.username
                response = jsonify("Success")

                global serverRestarted
                serverRestarted = False
                
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

            global serverRestarted
            serverRestarted = False

        session['email'] = email
        session['username'] = username

    return jsonify("success")

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)


# socket methods
def messageReceived(methods=['GET', 'POST']):
    print('Message was received!')

@socketio.on('store')
def storeData(session):
    print(session)

#join the room with somone you searched for
@socketio.on('join')
def on_join(data):
    if('email' in session and serverRestarted is False):
        email_check = User.query.filter_by(email=session['email']).first()
        username = Rooms.query.filter_by(username1=email_check.username).first()

        if email_check and username:
            path_name = data['path_name']
            room_number = path_name.split('/')[2]

            join_room(room_number)

            # socketio.emit('message_received', {'msg': email_check.username+' is online','user': email_check.username}, room=room_number,callback=messageReceived)

@socketio.on('connect')
def on_connect():
    if('email' in session and serverRestarted is False):
        print("Hello world! ... connected")
        email_check = User.query.filter_by(email=session['email']).first()


@socketio.on('disconnect')
def on_disconnect():
    print("Hello world! ... disconnected")

#sends message typed back to client side to be displayed with the person who sent it
@socketio.on('sending_message')
def send_to_user(json, methods=['GET', 'POST']):
    if('email' in session and serverRestarted is False):
        email_check = User.query.filter_by(email=session['email']).first()
        username = Rooms.query.filter_by(username1=email_check.username).first()

        if email_check and username:
            path_name = json['path_name']
            room_number = path_name.split('/')[2]
            
            conversation = Conversation.query.filter_by(room = room_number).first()

            message = Message(sender=email_check.username, message=json['message'])

            if(conversation.message):
                conversation.message.append(message)
            else:
                conversation.message = [message]
            
            db.session.commit()

            dict = {'user': "", 'msg': email_check.username+ ': '+ json['message']}
            
            emit('message_received', dict,room=room_number, broadcast=True)

            dict = {'user': email_check.username, 'msg': ""}

            emit('message_received', dict)