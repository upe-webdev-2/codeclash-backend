from codeclash_backend import socketio
from . import already_playing, dequeue_from_waiting, queue_to_waiting, create_room, find_room, delete_room, amount_players_waiting, in_waiting_room, remove_from_waiting_room
from ..routes.execute import execute_code
from ..routes.user import get_user
from ..routes.problem import rand_problem
from flask import request
from flask_socketio import close_room, emit

namespace = "/play"

@socketio.on('playerJoin', namespace = namespace)
def join_game(data):
    first_player_id = request.sid
    first_player_name = data.get("username")

    if already_playing(first_player_name):
        return

    if amount_players_waiting() >= 1:
        second_player_id, second_player_name = dequeue_from_waiting()
        room_name = f"{first_player_id} {second_player_id}"

        second_player_info = get_user(second_player_name)
        first_player_info = get_user(first_player_name)

        create_room(room_name, first_player_name, second_player_name)
        
        emit("finishedWaitingRoom", {"roomName" : room_name, "opponentName" : second_player_name, "opponentInfo" : second_player_info}, namespace = "/play")
        emit("finishedWaitingRoom", {"roomName" : room_name, "opponentName" : first_player_name, "opponentInfo" : first_player_info}, namespace = "/play", to = second_player_id)
    else:
        queue_to_waiting(first_player_id, first_player_name)

@socketio.on('playerLeave', namespace = namespace)
def player_leave(data):
    lost_player_id = request.sid
    lost_player_name = data.get("username")

    if in_waiting_room(lost_player_id, lost_player_name):
        remove_from_waiting_room(lost_player_id, lost_player_name)
        return

    room = find_room(username = lost_player_name, user_id = lost_player_id)

    if len(room) == 0:
        return

    room_name = room.get("roomName")
    room_players = room.get("roomInfo").get("players")

    won_player_name = room_players[1] if room_players[0] == lost_player_name else room_players[0]

    won_player_info = get_user(won_player_name)
    lost_player_info = get_user(lost_player_name)

    emit("finishedGame", {"wonPlayer" : won_player_name, "lostPlayer" : lost_player_name, "wonPlayerInfo" : won_player_info, "lostPlayerInfo" : lost_player_info}, namespace = "/play", to = room_name.split(" ")[0])
    emit("finishedGame", {"wonPlayer" : won_player_name, "lostPlayer" : lost_player_name, "wonPlayerInfo" : won_player_info, "lostPlayerInfo" : lost_player_info}, namespace = "/play", to = room_name.split(" ")[1])

    delete_room(room_name)
    close_room(room_name, namespace = "/play")

@socketio.on("disconnect", namespace = namespace)
def disconnect(data):
    disconnect_player_id = request.sid

    if in_waiting_room(player_id = disconnect_player_id):
        remove_from_waiting_room(disconnect_player_id)
        return

    room = find_room(user_id = disconnect_player_id)

    if len(room) == 0:
        return

    lost_player_name, won_player_name = None, None

    room_name = room.get("roomName")
    room_players = room.get("players")
    room_player_ids = room_name.split(" ")

    if room_player_ids[0] == disconnect_player_id:
        lost_player_name = room_players[0]
        won_player_name = room_players[1]
    else:
        lost_player_name = room_players[1]
        won_player_name = room_players[0]

    won_player_info = get_user(won_player_name)
    lost_player_info = get_user(lost_player_name)

    emit("finishedGame", {"wonPlayer" : won_player_name, "lostPlayer" : lost_player_name, "wonPlayerInfo" : won_player_info, "lostPlayerInfo" : lost_player_info}, namespace = "/play", to = room_name.split(" ")[0])
    emit("finishedGame", {"wonPlayer" : won_player_name, "lostPlayer" : lost_player_name, "wonPlayerInfo" : won_player_info, "lostPlayerInfo" : lost_player_info}, namespace = "/play", to = room_name.split(" ")[1])

    delete_room(room_name)
    close_room(room_name, namespace = "/play")


@socketio.on("playerWin", namespace = namespace)
def player_win(data):
    won_player_name = data.get("username")

    room = find_room(username = won_player_name)

    if len(room) == 0:
        # User not in a room. Maybe return an error?
        return

    room_name = room.get("roomName")
    room_players = room.get("roomInfo").get("players")

    lost_player_name = room_players[1] if room_players[0] == won_player_name else room_players[0]

    delete_room(room_name)

    won_player_info = get_user(won_player_name)
    lost_player_info = get_user(lost_player_name)

    emit("finishedGame", {"wonPlayer" : won_player_name, "lostPlayer" : lost_player_name, "wonPlayerInfo" : won_player_info, "lostPlayerInfo" : lost_player_info}, namespace = "/play", to = room_name)
    close_room(room_name)

@socketio.on("playerTest", namespace = namespace)
def player_test(data):
    user_code = data.get("userCode")
    player_name = data.get("username")
    room = find_room(username = player_name)
    problem_number = room.get("roomInfo").get("problemNumber")

    result = execute_code(user_code, problem_number, True)
    emit("playerTestResult", {**result})

@socketio.on("playerSubmit", namespace = namespace)
def player_test(data):
    user_code = data.get("userCode")
    player_name = data.get("username")
    room = find_room(username = player_name)
    problem_number = room.get("roomInfo").get("problemNumber")

    result = execute_code(user_code, problem_number)

    if result.get("passedAllCases"):
        player_win({"username" : player_name})
    else:
        emit("playerSubmitResult", {**result})