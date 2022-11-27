from typing import Union

from flask_socketio import emit, join_room, close_room
from flask import request
from ..routes.problem import rand_problem, specific_problem

waiting_room = []
rooms = {}

def find_room(room_name : str = None, username : str = None, user_id : str = None) -> dict:

    if room_name is not None:
        return rooms.get(room_name)

    if username is None and user_id is None:
        return {}

    for room in rooms.keys():
        room_info = rooms.get(room)
        players = room_info.get("players")
        
        if user_id is not None and user_id in room:
            return {"roomName" : room, "roomInfo" : room_info}

        if username is not None and username in players:
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

def in_waiting_room(player_id : str = None, player_name : str = None) -> bool:
    for p_info in waiting_room:
        p_id, p_name = p_info
        if player_id is not None and player_id == p_id:
            return True
        if player_name is not None and player_name == p_name:
            return True
    return False

def remove_from_waiting_room(player_id : str = None, player_name : str = None) -> Union[tuple, None]:
    for index, player_info in enumerate(waiting_room):
        p_id, p_name = player_info
        if player_id is not None and player_id == p_id:
            return waiting_room.pop(index)
        if player_name is not None and player_name == p_name:
            return waiting_room.pop(index)
    return None

def create_room(room_name : str, first_player_name : str, second_player_name : str):
    problem = rand_problem()
    rooms[room_name] = {"players" : [first_player_name, second_player_name], "problemNumber" : problem.get("problemNumber"), "problemInfo" : problem}

def delete_room(room_name : str):
    del rooms[room_name]

def reset_rooms():
    waiting_room.clear()
    rooms.clear()

from . import game, player