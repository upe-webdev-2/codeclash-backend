from codeclash_backend import socketio
from flask_socketio import emit, join_room
from . import find_room

namespace = "/play"

@socketio.on("readyGame", namespace = namespace)
def ready_game(data):
    room_name = data.get("roomName")
    join_room(room_name)

    room = find_room(room_name = room_name)
    problem = room.get("problemInfo")

    emit("startGame", {"problemInfo" : problem}, namespace = "/play")