from codeclash_backend import socketio
from flask_socketio import emit, join_room
from . import set_problem

namespace = "/play"

@socketio.on("readyGame", namespace = namespace)
def ready_game(data):
    room_name = data.get("roomName")
    join_room(room_name)

    problem = set_problem(room_name)

    emit("startGame", {"problemInfo" : problem}, namespace = "/play")