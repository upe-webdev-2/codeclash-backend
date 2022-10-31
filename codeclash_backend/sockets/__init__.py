from codeclash_backend import socketio
from flask_socketio import emit, join_room, close_room, rooms
from flask import request

all_rooms = {}

@socketio.on('connect')
def connect():
    if len(rooms()) > 1:
        return {'message' : "User is already connected to room"}
    
    for room in all_rooms.keys():
        if all_rooms.get(room) == 1:
            join_room(all_rooms.get(room))
            all_rooms[room] += 1
            print(f"Rooms after joining : {rooms()}")
            return {'message' : f"User connected, sent to room {room}"}
    
    join_room(request.sid)
    all_rooms[rooms()[-1]] = 1
    print(f"Rooms after joining : {rooms()}")
    return {'message': f'User connected, sent to room {rooms()[-1]}'}

@socketio.on('leave')
def disconnect(auth):
    print(f"Current user rooms before deletion: {rooms()}")
    if rooms()[0] in all_rooms.keys(): del all_rooms[rooms()[0]]
    print(f'User disconnected, destroyed room {rooms()[0]}')
    close_room(rooms()[0])
    return {'message' : f'User disconnected, destroyed room'}