# This is to be used for local testing. DONOT modify this file unless you have consulted the team. DONOT use this in production.

from SayLess import app, socketio
import eventlet
eventlet.monkey_patch()

if __name__ == "__main__":
    socketio.run(app,debug=True, host='localhost', port=8000)
    # app.run(debug=True, host='localhost', port=8000) 