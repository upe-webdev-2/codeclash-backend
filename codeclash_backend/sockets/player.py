from codeclash_backend import socketio
from . import already_playing, dequeue_from_waiting, queue_to_waiting, create_room, find_room, delete_room, amount_players_waiting
from flask import request
from flask_socketio import close_room, emit

@socketio.on('playerJoin', namespace = "/play")
def join_game(data):
    first_player_id = request.sid
    first_player_name = data.get("username")

    if already_playing(first_player_name):
        # Maybe send error?
        return

    if amount_players_waiting() >= 1:

        second_player_id, second_player_name = dequeue_from_waiting()
        room_name = f"{first_player_id} {second_player_id}"
        
        emit("finishedWaitingRoom", {"roomName" : room_name, "opponentName" : second_player_name}, namespace = "/play")
        emit("finishedWaitingRoom", {"roomName" : room_name, "opponentName" : first_player_name}, namespace = "/play", to = second_player_id)
        
        create_room(room_name, first_player_name, second_player_name)
    else:
        queue_to_waiting(first_player_id, first_player_name)

@socketio.on('playerLeave', namespace = "/play")
def player_leave(data):
    lost_player_id = request.sid
    lost_player_name = data.get("username")

    room_info = find_room(lost_player_name, lost_player_id)

    if len(room_info) == 0:
        # User not in a room. Maybe return an error?
        return

    room_name = room_info.get("room_name")
    room_players = room_info.get("players")

    won_player_name = room_players[1] if room_players[0] == lost_player_name else room_players[0]

    delete_room(room_name)

    emit("finishedGame", {"wonPlayer" : won_player_name, "lostPlayer" : lost_player_name}, namespace = "/play", to = room_name)
    close_room(room_name)

@socketio.on("playerWin", namespace = "/play")
def player_win(data):
    won_player_id = request.sid
    won_player_name = data.get("username")

    room_info = find_room(won_player_name, won_player_id)

    if len(room_info) == 0:
        # User not in a room. Maybe return an error?
        return

    room_name = room_info.get("room_name")
    room_players = room_info.get("players")

    lost_player_name = room_players[1] if room_players[0] == won_player_name else room_players[0]

    delete_room(room_name)

    emit("finishedGame", {"wonPlayer" : won_player_name, "lostPlayer" : lost_player_name}, namespace = "/play", to = room_name)
    close_room(room_name)