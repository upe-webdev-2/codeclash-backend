from codeclash_backend import socketio
from codeclash_backend.routes.problem import rand_problem
from flask_socketio import emit, join_room

@socketio.on("readyGame", namespace = "/play")
def ready_game(data):
    room_name = data.get("roomName")
    opponent_name = data.get("opponentName")
    join_room(room_name)
    emit("startGame", {"opponentName" : opponent_name, "roomName" : room_name, "problemInfo" : rand_problem()}, namespace = "/play")