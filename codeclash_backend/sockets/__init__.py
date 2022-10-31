from codeclash_backend import socketio
from flask_socketio import send, join_room, close_room

rooms = {}

@socketio.on('connect')
def connect(auth):
    if len(rooms) == 0:
        rooms[auth.roomName] = 1
        join_room(auth.roomName)
    else:
        for room in rooms.keys():
            if rooms[room] <= 1:
                rooms[room] += 1
                join_room(auth.roomName)
    send({'message': f'User connected, sent to room {auth.roomName}'})

@socketio.on('disconnect')
def disconnect(auth):
    rooms.remove(auth.roomName)
    close_room(auth.roomName)
    send({'message' : f'User disconnected, destroyed room {auth.roomName}'})