from flask_socketio import emit, join_room, close_room
from flask import request
from codeclash_backend.routes.problem import rand_problem

waiting_room = []
rooms = {}

def find_room(username = None, user_id = None) -> dict:
    if username is None and user_id is None:
        return {}

    for room in rooms.keys():
        if user_id in room or username in rooms.get(room):
            return {"room_name" : room, "players" : rooms.get(room)}
    
    return {}

def already_playing(username : str) -> bool:
    for user in waiting_room:
        _, searching_name = user
        if username == searching_name:
            return True
    
    for room in rooms.keys():
        if username in rooms.get(room):
            return True

    return False

def amount_players_waiting():
    return len(waiting_room)

def dequeue_from_waiting() -> tuple:
    return waiting_room.pop(0)

def queue_to_waiting(player_id : str, player_name : str):
    waiting_room.append((player_id, player_name))

def create_room(room_name : str, first_player_name : str, second_player_name : str):
    rooms[room_name] = [first_player_name, second_player_name]

def delete_room(room_name : str):
    del rooms[room_name]

from . import game, player