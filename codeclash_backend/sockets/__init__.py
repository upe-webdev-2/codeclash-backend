from unicodedata import name
from codeclash_backend import socketio
from flask_socketio import emit, join_room, close_room
from flask import request

waiting_room = []
rooms = {}

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
        
        rooms[room_name] = f"{first_player_name} {second_player_name}"
    else:
        waiting_room.append((first_player_id, first_player_name))

@socketio.on("readyGame", namespace = "/play")
def ready_game(data):
    room_name = data.get("roomName")
    opponent_name = data.get("opponentName")
    join_room(room_name)
    emit("startGame", {"opponentName" : opponent_name, "roomName" : room_name}, namespace = "/play")

@socketio.on('playerLeave', namespace = "/play")
def player_leave(data):
    lost_player_id = request.sid
    lost_player_name = data.get("username")
    won_player_name = None
    room_name = None

    for room in rooms.keys():
        if lost_player_id in room:
            room_name = room
            names = rooms.get(room).split(" ")
            del rooms[room]
            won_player_name = names[1] if names[0] == lost_player_name else names[0]
            break
    
    # Maybe send error?
    if room_name is None: return

    emit("finishedGame", {"wonPlayer" : won_player_name, "lostPlayer" : lost_player_name}, namespace = "/play", to = room)
    close_room(room_name)