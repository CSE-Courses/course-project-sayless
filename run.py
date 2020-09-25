from SayLess import app
# import eventlet
# eventlet.monkey_patch()

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=8000)