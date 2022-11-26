import unittest

from flask_socketio import SocketIO, send, emit, disconnect
from codeclash_backend import create_app, socketio, prisma
from codeclash_backend.sockets import in_waiting_room, find_room, reset_rooms

class TestSocketIO(unittest.TestCase):    
    def setUp(self) -> None:
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()
    
    def tearDown(self) -> None:
        self.ctx.pop()
        prisma.disconnect()
        reset_rooms()
    
    def test_connect(self):
        client = socketio.test_client(self.app, namespace = "/play")
        client2 = socketio.test_client(self.app, namespace = "/play")
        self.assertTrue(client.is_connected("/play"))
        self.assertTrue(client2.is_connected("/play"))
        self.assertNotEqual(client.eio_sid, client2.eio_sid)
        client.disconnect("/play")
        self.assertFalse(client.is_connected("/play"))
        self.assertTrue(client2.is_connected("/play"))
        client2.disconnect("/play")
        self.assertFalse(client2.is_connected("/play"))
    
    def test_player_join(self):
        client = socketio.test_client(self.app, namespace = "/play")
        client2 = socketio.test_client(self.app, namespace = "/play")

        client_name = "client@email.com"
        client2_name = "client2@mail.com"

        client.emit("playerJoin", {"username" : client_name}, namespace = "/play")
        client2.emit("playerJoin", {"username" : client2_name}, namespace = "/play")

        client_received = client.get_received(namespace = "/play")
        client2_received = client2.get_received(namespace = "/play")

        self.assertEqual(len(client_received), 1, "playerJoin is not emitting only 1 event")
        self.assertEqual(len(client2_received), 1, "playerJoin is not emitting only 1 event")

        self.assertEqual(client_received[0]['name'], 'finishedWaitingRoom', "playerJoin is not emitting finishedWaitingRoom")
        self.assertEqual(client2_received[0]['name'], 'finishedWaitingRoom', "playerJoin is not emitting finishedWaitingRoom")

        self.assertEqual(client_received[0]['args'][0].get("opponentName"), client2_name, "Client is not receiving correct opponent's name")
        self.assertEqual(client2_received[0]['args'][0].get("opponentName"), client_name, "Client is not receiving correct opponent's name")

        self.assertEqual(client_received[0]['args'][0].get("roomName"), client2_received[0]['args'][0].get("roomName"), "Clients are not in the same room.")
    
    def test_player_leave_waiting_room(self):
        # Check if playerLeave removes client from waitingRoom
        client = socketio.test_client(self.app, namespace = "/play")
        client_name = "client@email.com"

        client.emit("playerJoin", {"username" : client_name}, namespace = "/play")
        client.emit("playerLeave", {"username" : client_name}, namespace = "/play")

        self.assertFalse(in_waiting_room(player_name = client_name))

    def test_player_leave_not_joined(self):
        # Check if playerLeave works when player is not joined
        client = socketio.test_client(self.app, namespace = "/play")
        client_name = "client@email.com"
        client.emit("playerLeave", {"username" : client_name}, namespace = "/play")

    def test_player_leave_in_game(self):
        client = socketio.test_client(self.app, namespace = "/play")
        client_name = "client@email.com"

        client2 = socketio.test_client(self.app, namespace = "/play")
        client2_name = "client2@gmail.com"

        client.emit("playerJoin", {"username" : client_name}, namespace = "/play")
        client2.emit("playerJoin", {"username" : client2_name}, namespace = "/play")

        client.emit("playerLeave", {"username" : client_name}, namespace = "/play")

        self.assertEqual(find_room(client_name), {})
        self.assertEqual(find_room(client2_name), {})

        client_received = client.get_received(namespace = "/play")
        client2_received = client2.get_received(namespace = "/play")

        self.assertEqual(len(client_received), 2)
        self.assertEqual(len(client2_received), 2)

        self.assertEqual(client_received[1]["name"], "finishedGame")
        self.assertEqual(client2_received[1]["name"], "finishedGame")
    
    def test_ready_game(self):
        client = socketio.test_client(self.app, namespace = "/play")
        client_name = "client@email.com"

        client2 = socketio.test_client(self.app, namespace = "/play")
        client2_name = "client2@email.com"

        client.emit("playerJoin", {"username" : client_name}, namespace = "/play")
        client2.emit("playerJoin", {"username" : client2_name}, namespace = "/play")

        room_name = client.get_received(namespace = "/play")[0]["args"][0].get("roomName")
        
        client.emit("readyGame", {"roomName" : room_name}, namespace = "/play")
        client2.emit("readyGame", {"roomName" : room_name}, namespace = "/play")

        client_received = client.get_received(namespace = "/play")
        client2_received = client2.get_received(namespace = "/play")

        self.assertEqual(client_received[-1]["name"], "startGame")
        self.assertEqual(client2_received[-1]["name"], "startGame")

        self.assertIn("problemInfo", client_received[-1]["args"][0])
        self.assertIn("problemInfo", client2_received[-1]["args"][0])
    
    def test_player_test(self):
        client = socketio.test_client(self.app, namespace = "/play")
        client_name = "client@email.com"

        client2 = socketio.test_client(self.app, namespace = "/play")
        client2_name = "client2@email.com"

        client.emit("playerJoin", {"username" : client_name}, namespace = "/play")
        client2.emit("playerJoin", {"username" : client2_name}, namespace = "/play")

        room_name = client.get_received(namespace = "/play")[0]["args"][0].get("roomName")
        
        client.emit("readyGame", {"roomName" : room_name}, namespace = "/play")
        client2.emit("readyGame", {"roomName" : room_name}, namespace = "/play")

        starter_code = client.get_received(namespace = "/play")[0]["args"][0].get("problemInfo").get("starterCode")
        starter_code += "\n\treturn 1"

        client.emit("playerTest",  {"username" : client_name, "userCode" : starter_code}, namespace = "/play")

        self.assertEqual(client.get_received(namespace = "/play")[0]["name"], "playerTestResult")
    
    def test_player_submit(self):
        client = socketio.test_client(self.app, namespace = "/play")
        client_name = "client@email.com"

        client2 = socketio.test_client(self.app, namespace = "/play")
        client2_name = "client2@email.com"

        client.emit("playerJoin", {"username" : client_name}, namespace = "/play")
        client2.emit("playerJoin", {"username" : client2_name}, namespace = "/play")

        room_name = client.get_received(namespace = "/play")[0]["args"][0].get("roomName")
        
        client.emit("readyGame", {"roomName" : room_name}, namespace = "/play")
        client2.emit("readyGame", {"roomName" : room_name}, namespace = "/play")

        starter_code = client.get_received(namespace = "/play")[0]["args"][0].get("problemInfo").get("starterCode")
        starter_code += "\n\treturn 1"

        client.emit("playerSubmit",  {"username" : client_name, "userCode" : starter_code}, namespace = "/play")

        self.assertEqual(client.get_received(namespace = "/play")[0]["name"], "playerSubmitResult")