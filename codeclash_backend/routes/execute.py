from flask import Blueprint
execute = Blueprint('execute', __name__)

@execute.route('/', methods = ["POST"])
def index():
    return {
        
    }