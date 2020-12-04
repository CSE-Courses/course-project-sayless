import os
import bcrypt
import urllib.parse 

import eventlet
eventlet.monkey_patch()

from SayLess.helpers import *

from flask import Flask, flash,render_template, request, Response, redirect, jsonify, session, make_response, url_for,send_from_directory
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
from werkzeug.utils import secure_filename

#images directory : changes on /profile for rendering html with src path
IMAGES_CONTAINER = "images"
#type of files we allow: file saving happens in /avi
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
app.config['MAIL_PASSWORD'] = get_secret("pass")
mail = Mail(app)

params = urllib.parse.quote_plus(get_secret("DB"))

app.config.from_pyfile('config.py', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect={}".format(params)

app.config['MYSQL_CHARSET'] = 'utf8mb4'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db.init_app(app)
db.create_all()

socketio = SocketIO(app)

minify(app=app, html=True, js=True, cssless=True)

serverRestarted = True
Character_Limit = 25

create_container_sample(IMAGES_CONTAINER)

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

@app.route('/userbio', methods=['GET'])
def userbio():
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
        chatting_with = ""
        bio = ""
        if email_check:
            bio = email_check.bio

        profile = Profile.query.filter_by(email=session['email']).first()
        file_name = "data:image/jpeg;base64,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"

        if profile:
            # settings link for the accessible file
            file_name = "https://sayless.blob.core.windows.net/images/" + profile.filename

        return render_template('bio.html', username=email_check.username, bio=bio,filename=file_name)
    return redirect('/')



@app.route('/bio/<string:room_number>', methods=['GET', 'POST'])
def bio(room_number):
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
        chatting_with = ""
        bio = ""
        room = Rooms.query.filter_by(room = room_number).first()
        if room.username1 == email_check.username:
            chatting_with = room.username2

        else:
            chatting_with = room.username1
        other = User.query.filter_by(username=chatting_with).first()
        bio = other.bio
        # if(email_check and email_check.bio):
        #     bio = email_check.bio
        profile = Profile.query.filter_by(email=other.email).first()
        file_name = "data:image/jpeg;base64,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"

        if profile:
            # settings link for the accessible file
            file_name = "https://sayless.blob.core.windows.net/images/" + profile.filename

        return render_template('bio.html', username=chatting_with, bio=bio,filename=file_name)

    return redirect('/')

@app.route('/search', methods=['POST'])
def search():
    if('email' in session):
        users = []

        all = db.session.query(User).all()

        current_user = User.query.filter_by(email=session['email']).first()

        blocked_list = current_user.blocked

        for user in all:
            if user.email != session['email']:
                to_append = True
                for blocked in blocked_list:
                    if(blocked.blocked_user == user.username):
                        to_append = False
                        break
                
                if(to_append):
                    users.append(user.username)

        return jsonify(users)
    else:
        return ""

@app.route("/deleteacc", methods=['GET','POST'])
def delete():
    global serverRestarted

    if(serverRestarted):
        session.clear()
        serverRestarted = False
        return redirect("/login")
    if request.method == 'GET' and 'email' not in session:
        print("Invalid access")
        return redirect("/login")
    elif request.method == 'POST' and 'email' in session:
        # delete the user
        user = User.query.filter_by(email=session['email']).first()

        if(user):
            db.session.delete(user)
            db.session.commit()

            # delete the roooms
            rooms = Rooms.query.filter_by(username1=user.username)

            for room in rooms:
                db.session.delete(room)
                db.session.commit()

                # delete from conversation
                conversation = Conversation.query.filter_by(room=room.room)
                for conv in conversation:
                    db.session.delete(conv)
                    db.session.commit()
            
            rooms_2 = Rooms.query.filter_by(username2=user.username)

            for room in rooms_2:
                db.session.delete(room)
                db.session.commit()

                # delete from conversation
                conversation = Conversation.query.filter_by(room=room.room)
                for conv in conversation:
                    db.session.delete(conv)
                    db.session.commit()

            # delete from profile
            profile = Profile.query.filter_by(email = user.email).first()

            if(profile):
                db.session.delete(profile)
                db.session.commit()

            # delete from messages
            messages = Message.query.filter_by(sender=user.username)
            for message in messages:
                db.session.delete(message)
                db.session.commit()

        return jsonify("success")
  
    return render_template('deleteacc.html')

@app.route("/block", methods=['GET','POST'])
def block():
    global serverRestarted

    if(serverRestarted):
        session.clear()
        serverRestarted = False
        return redirect("/login")

    if request.method == 'GET' and 'email' in session:
        # Do stuff for get request
        print("In GET")
        user = User.query.filter_by(email=session['email']).first()
        blocked_users = user.blocked

        blocked = []
        for block in blocked_users:
            blocked.append(block.blocked_user)

        return render_template('block.html', blocked_users=blocked)
    elif request.method == 'GET' and 'email' not in session:
        print("Invalid access")
        return redirect("/login")
    else:
        # In Post request
        print("In POST")

        data = request.form.get("username")
        
        user = User.query.filter_by(email=session['email']).first()
        block = Block(blocked_user = data)

        if(user.blocked):
            user.blocked.append(block)
        else:
            user.blocked = [block]
        
        db.session.commit()

        return jsonify("Success")

@app.route("/unblock", methods=['POST'])
def unblock():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()

        user_to_unblock = request.form.get("username")

        print(user_to_unblock)

        for blocked in user.blocked:
            if blocked.blocked_user == user_to_unblock:
                user.blocked.remove(blocked)
                db.session.commit()
                return jsonify("Success")

        return jsonify("Fail")
    elif 'email' not in session:
        return jsonify("Login")
    else:
        return jsonify("Error")

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
        file_name = "data:image/jpeg;base64,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"
        email = User.query.filter_by(email=session['email']).first()
        #This is for getting image path
        profile = Profile.query.filter_by(email=session['email']).first()
        if(email):
            username = email.username
            first_name = email.first_name
            last_name = email.last_name
            Bio = email.bio
            if Bio is None:
                Bio = ""
        if profile:
            # settings link for the accessible file
            file_name = "https://sayless.blob.core.windows.net/images/" + profile.filename
            
        return render_template('profile.html', username=username, FirstName=first_name, LastName=last_name , bio=Bio,filename=file_name)
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
#checking for valid file types          
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        profile = Profile.query.filter_by(email=session['email']).first()
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
        blocked_users = email_check.blocked

        if(email_check.username == username):
            return jsonify({'Cannot_Talk':username})

        if username_check is None:
            return jsonify({'Invalid_user':"invalid"})

        for blocked in blocked_users:
            if(blocked.blocked_user == username):
                return jsonify({'Blocked User':username})

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

    blocked_list = email_check.blocked

    users1 = Rooms.query.filter_by(username1=email_check.username)
    users2 = Rooms.query.filter_by(username2=email_check.username)

    #Now for username1 we check if they have new message as well
    for room in users1:
        to_append = True
        for blocked in blocked_list:
            if(room.username2 == blocked.blocked_user):
                to_append = False
                break

        if room.username2 not in data and to_append:
            data[room.username2] = []
            data[room.username2].append(room.room)
            data[room.username2].append(room.new_message)
            
    #don't think this ever even runs? but add in an always false just in case for now?
    for room in users2:
        to_append = True
        for blocked in blocked_list:
            if(room.username1 == blocked.blocked_user):
                to_append = False
                break

        if room.username1 not in data and to_append:
            data[room.username1] = []
            data[room.username1].append(room.room)
            data[room.username1].append(0)
         

    return jsonify(data)

@app.route('/suggestedchats', methods=['POST'])
def suggested():
    data = []

    email = session['email']
    email_check = User.query.filter_by(email=email).first()

    if(email_check is None):
        return jsonify(data) 

    blocked_list = email_check.blocked
    
    users1 = Rooms.query.filter_by(username1=email_check.username)
    users2 = Rooms.query.filter_by(username2=email_check.username)

    allUsers = db.session.query(User)

    for user in allUsers:
        if(email_check.username == user.username):
            continue
        
        to_append = True
        for blocked in blocked_list:
            if(user.username == blocked.blocked_user):
                to_append = False
                break
        
        if not to_append:
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

        history = []

        # check history of messages and load all of them
        conversation = Conversation.query.filter_by(room = room_number).first()
        room = Rooms.query.filter_by(room = room_number).first()

        # handling case of when user tries to open chat with blocked user
        blocked_users = email_check.blocked

        for blocked in blocked_users:
            if(email_check.username == room.username1):
                if(room.username2 == blocked.blocked_user):
                    return redirect("/")
            else:
                if(room.username1 == blocked.blocked_user):
                    return redirect("/")

        if(conversation):
            messages = conversation.message

            for message in messages:
                if(message.sender == email_check.username):
                    history.append([message.message, False])
                else:
                    history.append([message.message, True])

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
#for now it uploads image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/avi', methods=['GET', 'POST'])
def edit_profile():
    global serverRestarted

    if(serverRestarted):
        session.clear()
        serverRestarted = False
        return redirect("/login")
    #Here will be where files are uploaded and saved to the images folder
    if request.method == 'POST' and 'email' in session:
        # check if the post request has the file part
        print("getting file stuff.....: ",request.files)
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            i = filename.index('.')
            N = 17
            hashedWord = sha256(''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N)).encode('utf-8')).hexdigest()
            filename = filename[:i] + '-' + session['email'] +hashedWord+ filename[i:]

            # blob storage for image
            my_content_settings = ContentSettings(content_type="image/"+filename.rsplit('.', 1)[1].lower())
            blob_client = blob_service_client.get_container_client(IMAGES_CONTAINER).get_blob_client(filename)
            blob_client.upload_blob(file.read(), blob_type="BlockBlob", content_settings=my_content_settings)
            
            image = Profile.query.filter_by(email=session['email']).first()

            #adding the image file name to the database table Profile if it doesn't exist
            if image:
                #update filename
                image.filename = filename
                db.session.commit()
            else:
                info = Profile(email=session['email'],filename=filename)
                db.session.add(info)
                db.session.commit()
        elif file and not allowed_file(file.filename):
            return redirect("/avi")
        
        return redirect("/profile")
            
    # verify if the current user is allowed to access the room

    if request.method == 'GET' and 'email' in session:
        # Do stuff for get request
        print("Rendering edit profile page")

        return render_template('avi.html')
        
    elif request.method == 'GET' and 'email' not in session:
        print("Invalid access")
        return redirect("/login")
    
    return redirect("/avi")


@app.route('/character_limit', methods=['POST'])
def character_limit():
    if 'email' in session:
        # character limit on the message
        split_message = request.get_data().split()

        chars = 0

        for m in split_message:
            for char in m.decode():
                if not is_emoji(char):
                    chars += 1

        if(chars <= Character_Limit):
            dictionary = {'Success':(Character_Limit - chars), 'limit': Character_Limit}
            return jsonify(dictionary)
        else:
            dictionary = {'limit': Character_Limit, "Exceeded" : (chars - Character_Limit)}
            return jsonify(dictionary)


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
        path_name = data['path_name']
        room_number = path_name.split('/')[2]
        email_check = User.query.filter_by(email=session['email']).first()
        username = Rooms.query.filter_by(username1=email_check.username , room=room_number).first()

        if email_check and username:
            #When a username 1 joins a room notify server that new messages are read
            username.new_message = 0
            db.session.commit()
            

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
        path_name = json['path_name']
        room_number = path_name.split('/')[2]
        email_check = User.query.filter_by(email=session['email']).first()
        username = Rooms.query.filter_by(username1=email_check.username , room=room_number).first()
        num = 0
      
        if email_check and username:
            #set the other person to have new messages for now
            print(username.username2)
            receiver = Rooms.query.filter_by(username1=username.username2 , room=room_number).first()
            print(receiver)
            num = receiver.new_message + 1
            receiver.new_message = num
            
            
            conversation = Conversation.query.filter_by(room = room_number).first()

            # character limit on the message
            split_message = json['message'].split()

            chars = 0

            for m in split_message:
                for char in m:
                    if not is_emoji(char):
                        chars += 1

            # current character limit is 50. Length of more than 50 is currently denied. But will possibly be changed once leaderboard is implemented.
            if(chars > Character_Limit):
                dict = {'user': "character_limit_error", 'msg': email_check.username+ ': '+ json['message'], 'limit': Character_Limit, "exceeded" : (chars - Character_Limit)}
                emit('message_received', dict,room=room_number)
            else:
                message = Message(sender=email_check.username, message=json['message'])

                if(conversation.message):
                    conversation.message.append(message)
                else:
                    conversation.message = [message]
                
                db.session.commit()

                dict = {'user': "", 'msg': email_check.username+ ': '+ json['message']}
                
                emit('message_received', dict,room=room_number, broadcast=True)

            join_room(json['target'])

            dict = {'room_number' : room_number , 'number' : num}

            emit('new_message' , dict , room=json['target'] , broadcast=True , include_self=False)

            leave_room(json['target'])


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

#If the person is already in the chat, set new messages back to false
@socketio.on('chat_open')
def chat_open(data):
     if('email' in session and serverRestarted is False):
        email_check = User.query.filter_by(email=session['email']).first()
        username = Rooms.query.filter_by(username1=email_check.username).first()
        if email_check and username:
            username.new_message = 0
            db.session.commit()


