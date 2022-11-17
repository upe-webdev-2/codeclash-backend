import os
from flask import Flask
from flask_socketio import SocketIO
from prisma import Prisma

prisma = Prisma()
app = Flask(__name__)

socketio = SocketIO(cors_allowed_origins = "*")

def create_app():
    """Create an application."""

    debug = os.environ.get("IS_DEBUG")

    app.debug = True if debug == "TRUE" else False
    app.config['SECRET_KEY'] = os.environ.get("SOCKET_IO_KEY")

    import codeclash_backend.routes
    socketio.init_app(app)
    import codeclash_backend.sockets
    return app