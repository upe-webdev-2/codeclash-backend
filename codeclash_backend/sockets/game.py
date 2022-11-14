from codeclash_backend import socketio
from flask_socketio import emit, join_room
from . import set_problem

namespace = "/play"

@socketio.on("readyGame", namespace = namespace)
def ready_game(data):
    room_name = data.get("roomName")
    opponent_name = data.get("opponentName")
    join_room(room_name)

    problem = set_problem(room_name)

    emit("startGame", {"opponentName" : opponent_name, "roomName" : room_name, "problemInfo" : problem}, namespace = "/play")
    print(f"Problem ID: {problem.get('id')}")