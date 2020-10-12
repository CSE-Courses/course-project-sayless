# This is going to be used in deployment to initialize app. DONOT modify this file unless you have consulted the team

from SayLess import app, socketio
import eventlet
eventlet.monkey_patch()

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0',port=443)
    # app.run()