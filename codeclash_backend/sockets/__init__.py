from codeclash_backend import socketio

@socketio.on('connect')
def connect(auth):
    print(auth)
    emit('test_connection', {'data': 'connected'})

@socketio.on('disconnect')
def disconnect(auth):
    print(auth)
    emit('test_disconnect', {'data' : 'disconnected'})