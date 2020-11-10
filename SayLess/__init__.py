import os
import bcrypt
import urllib.parse 

import eventlet
eventlet.monkey_patch()

from SayLess.helpers import *

from flask import Flask, render_template, request, Response, redirect, jsonify, session, make_response, url_for
from flask_socketio import SocketIO, leave_room, join_room, send, emit
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_mail import Message as M

from flask_minify import minify

from SayLess.database import *
from hashlib import *
import random
import string
from datetime import timedelta

# create the flask app
app = Flask(__name__, static_url_path='', static_folder='../statics', template_folder='../templates')
app.config.from_mapping(
    SECRET_KEY='CSE'
)

#SET UP TO USE FLASK MAIL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'sayless442@gmail.com'
#app.config['MAIL_PASSWORD'] = get_secret("pass")
mail = Mail(app)

#params = urllib.parse.quote_plus(get_secret("DB"))

app.config.from_pyfile('config.py', silent=True)
#app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect={}".format(params)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rileybur:50216039@tethys.cse.buffalo.edu:3306/rileybur_db'
app.config['MYSQL_CHARSET'] = 'utf8mb4'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db.init_app(app)
db.create_all()

socketio = SocketIO(app)

minify(app=app, html=True, js=True, cssless=True)

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
        
        email = session['email']
        email_check = User.query.filter_by(email=email).first()

        bio = ""

        if(email_check and email_check.bio):
            bio = email_check.bio

        return render_template('home.html', username=email_check.username, bio=bio)
    elif request.method == 'GET' and 'email' not in session:
        print("Invalid Login")
        return redirect("/login")
    else:
        # Do stuff for post request
        print("In POST")

    return redirect('/signup')

@app.route('/search', methods=['POST'])
def search():
    if('email' in session):
        users = []

        all = db.session.query(User).all()

        for user in all:
            if user.email != session['email']:
                users.append(user.username)

        return jsonify(users)
    else:
        return ""

@app.route("/logout", methods=['GET'])
def logout():
    global serverRestarted

    if(serverRestarted):
        session.clear()
        serverRestarted = False
        return redirect("/login")

    if request.method == 'GET' and 'email' in session:
        # Do stuff for get request
        print("In GET")

        session.clear()

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
        Bio = ""

        email = User.query.filter_by(email=session['email']).first()
        if(email):
            username = email.username
            first_name = email.first_name
            last_name = email.last_name
            Bio = email.bio
            if Bio is None:
                Bio = ""

        return render_template('profile.html', username=username, FirstName=first_name, LastName=last_name , bio=Bio)
    elif request.method == 'GET' and 'email' not in session:
        print("Invalid access")
        return redirect("/login")
    else:

        # In Post request
        print("In POST")

        form_data = request.form

        email = User.query.filter_by(email=session['email']).first()
        
        if(email):
            updates = ""

            if(form_data.get("firstname") != ""):
                email.first_name = form_data.get("firstname")
                db.session.commit()
                updates += "First Name, "
            
            if(form_data.get("lastname") != ""):
                email.last_name = form_data.get("lastname")
                db.session.commit()
                updates += "Last Name, "
            
            if(form_data.get("password") != ""):
                password = form_data.get("password")

                if len(password) < 8:
                    return jsonify("password too short")
                else:
                    password = password.encode('utf-8')
                    password = bcrypt.hashpw(password, bcrypt.gensalt())
                    email.password = password
                    db.session.commit()
                    updates += "Password, "
            
            if(form_data.get("username") != ""):
                rooms = Rooms.query.filter_by(username1=email.username)
                rooms2 = Rooms.query.filter_by(username2=email.username)

                for room in rooms:
                    room.username1 = form_data.get("username")

                for room in rooms2:
                    room.username2 = form_data.get("username")

                messages = Message.query.filter_by(sender=email.username)
                
                for message in messages:
                    message.sender = form_data.get("username")
                
                email.username = form_data.get("username")

                session['username'] = form_data.get("username")
                session['username2'] = form_data.get("username")
                
                db.session.commit()
                updates += "Username, "
            
            if(form_data.get("bio") != ""):
                bio = form_data.get("bio")
                email.bio = form_data.get("bio")
                db.session.commit()
                updates += "Bio, "

            if(updates == ""):
                return jsonify("Nothing Updated")

            return jsonify(updates.rstrip()[:-1] + " ")
        else:
            return jsonify("Undefined")


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

        email = session['email']
        email_check = User.query.filter_by(email=email).first()

        bio = ""

        if(email_check and email_check.bio):
            bio = email_check.bio

        return render_template('home.html', username=email_check.username, bio=bio)
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
            #random string generator
            line = username + session['username']
            N = 17
            hashedWord = sha256(''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)).encode('utf-8')).hexdigest()
            currentroom = str(hashedWord)
            me = Rooms(username1 = session['username'], username2 = username, room = currentroom )
            me2 = Rooms(username1 = username, username2 = session['username'], room = currentroom )
            db.session.add(me)

            db.session.add(me2)
            db.session.commit()
        elif username_check2:
            # if the search user is username1 then we enter here
            currentroom = username_check2.room
        else:
            currentroom = username_check1.room
        resp = make_response(jsonify({'Success':currentroom}))

        conversation = Conversation.query.filter_by(room=currentroom).first()
        if(conversation is None and currentroom != "DUMMY"):
            conversation = Conversation(room = currentroom)
            db.session.add(conversation)
            db.session.commit()
        
        return resp

    return redirect('home.html')

@app.route('/openchats', methods=['POST'])
def open():
    data = {}

    email = session['email']
    email_check = User.query.filter_by(email=email).first()

    if(email_check is None):
        return jsonify(data) 

    users1 = Rooms.query.filter_by(username1=email_check.username)
    users2 = Rooms.query.filter_by(username2=email_check.username)

    for room in users1:
        if room.username2 not in data:
            data[room.username2] = room.room

    for room in users2:
        if room.username1 not in data:
           data[room.username1] = room.room

    return jsonify(data)

@app.route('/suggestedchats', methods=['POST'])
def suggested():
    data = []

    email = session['email']
    email_check = User.query.filter_by(email=email).first()

    if(email_check is None):
        return jsonify(data) 
    
    users1 = Rooms.query.filter_by(username1=email_check.username)
    users2 = Rooms.query.filter_by(username2=email_check.username)

    allUsers = db.session.query(User)

    for user in allUsers:
        if(email_check.username == user.username):
            continue
        
        check = False
        for room in users1:
            if room.username2 == user.username:
                check = True
                break
        
        if check == True:
            continue
            
        for room in users2:
            if room.username1 == user.username:
                check = True
                break
        
        if check == True:
            continue

        data.append(user.username)
        
        if(len(data) >= 3):
            break

    return jsonify(data)

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

        history = {}

        # check history of messages and load all of them
        conversation = Conversation.query.filter_by(room = room_number).first()
        room = Rooms.query.filter_by(room = room_number).first()

        if(conversation):
            messages = conversation.message

            for message in messages:
                if(message.sender == email_check.username):
                    history[message.message] = False
                else:
                    history[message.message] = True

        chatting_with = ""

        if room.username1 == email_check.username:
            chatting_with = room.username2
        else:
            chatting_with = room.username1

        return render_template('chat.html', messages=history, user=chatting_with)
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

@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'GET':
        # render reset_request.html
        return render_template('reset_request.html')

    else:
        # Do stuff for post request
        form_data = request.form
        email = replace(form_data.get("email"))

        email_check = User.query.filter_by(email=email).first()

        # either way return succes but if it is an email, send an email with a url attached
        # said url expires in 10 minutes 
        if email_check != None:

            # call our create token method to create a token and add it to the email as part pf the url
            token = email_check.create_token()
          
            receiver_email = email  # Enter receiver address
            
            # if the email is in the DB but not actually an email this shouldn't cause any issues
            # they just won't get their email cuase hey your email isn't real yah dope
            # could add in that checks the return code and says hey your email is valid if we want
            msg = M('Reset Password', sender='sayless442@gmail.com', recipients=[receiver_email])
            msg.body = f'''Follow this link to reset your password. This link will expire in 10 minutes, after that you must re-request a password reset.
            {url_for('reset_pass' , token=token , _external=True)}
            '''
            mail.send(msg)
           

            return jsonify("Success")
    
    return jsonify("Success")

@app.route('/reset_pass/<string:token>', methods=['GET', 'POST'])
def reset_pass(token):
    if request.method == 'GET':
        user = User.correct_token(token)
        #if the token is still valid user will not be none
        # If expired user wil be none and we redirect them back to the request page
        if user is None:
            return redirect(url_for('reset_request'))
        user_id = user.id
        #send in the token and the user id assocaited with the user 
        #this can be changed later on to just use the token but I just did it like this for some reason atm
        return render_template('reset_password.html' , token=token , user_id=user_id)

    #if its a post request they are changing the password
    #so get the info from the form, along with the id of the user changing their password
    #verify passwords is long enough, matches, and the user exists(just to be safe)
    #if all is good encrypt the entered password and change it in the database
    else:
        form_data = request.form
        confirm = replace(form_data.get("confirm"))
        password = replace(form_data.get("password"))
        user_id = replace(form_data.get("user_id"))
        use = User.query.filter_by(id=user_id).first()

        # could add another check to  verify the password isn't the same as the current
        # but that is up to the group
        if len(password) < 8:
            return jsonify("password too short")
        elif password != confirm:
            return jsonify("password does not match")
        elif use is None:
            return jsonify("user_error")
        else:
            password = password.encode('utf-8')
            password = bcrypt.hashpw(password, bcrypt.gensalt())
            use.password = password
            db.session.commit()
            return jsonify("Success")

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

@app.route('/avi', methods=['GET', 'POST'])
def edit_profile():
    global serverRestarted

    if(serverRestarted):
        session.clear()
        serverRestarted = False
        return redirect("/login")

    # verify if the current user is allowed to access the room

    if request.method == 'GET' and 'email' in session:
        # Do stuff for get request
        print("Rendering edit profile page")

        return render_template('avi.html')
        
    elif request.method == 'GET' and 'email' not in session:
        print("Invalid access")
        return redirect("/login")
    else:
        # Do stuff for post request
         print("In POST")

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


#Sends a notification of starting a chat to another user
#Sends them the creater of the chat, whom they wish to start with , and the id of teh room created for the button
@socketio.on('sending_notification')
def send_notification(data):
    join_room(data["room"])
    dict = {'creating_user' : data['username'] , 'receive_user' :  data['room'] , 'room_id' : data['chat_id']}
    emit ("notification_received" , dict , broadcast=True, room=data['room'] , include_self=False)
    leave_room(data["room"])


#Create my personal notification room
@socketio.on('create_notify')
def create_notify(data):
    room_name = data['username']
    join_room(room_name)