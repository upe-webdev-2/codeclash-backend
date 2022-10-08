from competitive_programming_backend import app

@app.route('/')
def index():
    return "Hello World!"