import os
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

socketio = SocketIO(cors_allowed_origins = "*")

def create_app(debug = False):
    """Create an application."""
    app.debug = debug
    app.config['SECRET_KEY'] = os.environ.get("SOCKET_IO_KEY")

    import codeclash_backend.routes
    socketio.init_app(app)
    import codeclash_backend.sockets
    return app