# This is going to be used in deployment to initialize app. DONOT modify this file unless you have consulted the team

from SayLess import app, socketio

if __name__ == "__main__":
    socketio.run(app)
    # app.run()