import os
from codeclash_backend import create_app, socketio
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == '__main__':

    port = 5000 if os.environ.get("PORT") is None else int(os.environ.get("PORT"))

    socketio.run(app, host = "0.0.0.0", port = port)