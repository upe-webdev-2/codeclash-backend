from flask_socketio import emit, join_room, close_room
from flask import request
from ..routes.problem import rand_problem, specific_problem

waiting_room = []
rooms = {}

def find_room(username = None, user_id = None) -> dict:
    if username is None and user_id is None:
        return {}

    for room in rooms.keys():
        room_info = rooms.get(room)
        players = room_info.get("players")
        problem_id = room_info.get("problemID")
        if user_id in room or username in players:
            return {"roomName" : room, "roomInfo" : room_info}
    
    return {}

def already_playing(username : str) -> bool:
    for user in waiting_room:
        _, searching_name = user
        if username == searching_name:
            return True
    
    for room in rooms.keys():
        if username in rooms.get(room).get("players"):
            return True

    return False

def amount_players_waiting():
    return len(waiting_room)

def dequeue_from_waiting() -> tuple:
    return waiting_room.pop(0)

def queue_to_waiting(player_id : str, player_name : str):
    waiting_room.append((player_id, player_name))

def create_room(room_name : str, first_player_name : str, second_player_name : str):
    rooms[room_name] = {"players" : [first_player_name, second_player_name], "problemID" : None}

def delete_room(room_name : str):
    del rooms[room_name]

def set_problem(room_name : str):
    room = rooms.get(room_name)
    problem = None
    if room.get("problemID") is None:
        problem = rand_problem()
        room["problemID"] = problem.get("id")
    else:
        problem = specific_problem(room.get("problemID"))
    return problem

from . import game, player