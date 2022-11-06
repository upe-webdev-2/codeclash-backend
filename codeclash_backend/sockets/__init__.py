from unicodedata import name
from codeclash_backend import socketio
from flask_socketio import emit, join_room, close_room
from flask import request
from codeclash_backend.routes.problem import rand_problem

waiting_room = []
rooms = {}

def find_room(rooms = dict, username = None, user_id = None) -> dict:
    if username is None and user_id is None:
        return {}

    for room in rooms.keys():
        if user_id in room or username in rooms.get(room):
            return {"room_name" : room, "players" : rooms.get(room)}
    
    return {}

def already_playing(username : str, waiting_room : list, rooms : dict) -> bool:
    for user in waiting_room:
        _, searching_name = user
        if username == searching_name:
            return True
    
    for room in rooms.keys():
        if username in rooms.get(room):
            return True

    return False

@socketio.on('joinGame', namespace = "/play")
def join_game(data):
    first_player_id = request.sid
    first_player_name = data.get("username")

    if already_playing(first_player_name, waiting_room, rooms):
        # Maybe send error?
        return

    if len(waiting_room) >= 1:

        second_player_id, second_player_name = waiting_room.pop(0)
        room_name = f"{first_player_id} {second_player_id}"
        
        emit("finishedWaitingRoom", {"roomName" : room_name, "opponentName" : second_player_name}, namespace = "/play")
        emit("finishedWaitingRoom", {"roomName" : room_name, "opponentName" : first_player_name}, namespace = "/play", to = second_player_id)
        
        rooms[room_name] = [first_player_name, second_player_name]
    else:
        waiting_room.append((first_player_id, first_player_name))

@socketio.on("readyGame", namespace = "/play")
def ready_game(data):
    room_name = data.get("roomName")
    opponent_name = data.get("opponentName")
    join_room(room_name)
    emit("startGame", {"opponentName" : opponent_name, "roomName" : room_name, "problemInfo" : rand_problem()}, namespace = "/play")

@socketio.on('playerLeave', namespace = "/play")
def player_leave(data):
    lost_player_id = request.sid
    lost_player_name = data.get("username")

    room_info = find_room(rooms, lost_player_name, lost_player_id)

    if len(room_info) == 0:
        # User not in a room. Maybe return an error?
        return

    room_name = room_info.get("room_name")
    room_players = room_info.get("players")

    won_player_name = room_players[1] if room_players[0] == lost_player_name else room_players[0]

    del rooms[room_name]

    emit("finishedGame", {"wonPlayer" : won_player_name, "lostPlayer" : lost_player_name}, namespace = "/play", to = room_name)
    close_room(room_name)

@socketio.on("playerWin", namespace = "/play")
def player_leave(data):
    won_player_id = request.sid
    won_player_name = data.get("username")

    room_info = find_room(rooms, won_player_name, won_player_name)

    if len(room_info) == 0:
        # User not in a room. Maybe return an error?
        return

    room_name = room_info.get("room_name")
    room_players = room_info.get("players")

    lost_player_name = room_players[1] if room_players[0] == won_player_name else room_players[0]

    del rooms[room_name]

    emit("finishedGame", {"wonPlayer" : won_player_name, "lostPlayer" : lost_player_name}, namespace = "/play", to = room_name)
    close_room(room_name)