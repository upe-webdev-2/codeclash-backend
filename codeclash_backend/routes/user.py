from codeclash_backend import prisma
from flask import Blueprint

user = Blueprint('user', __name__)

def get_user(email):
    data = prisma.user.find_first(where = {
        "email" : email
    })

    if data is None:
        return None

    return data.dict()

@user.route('/<string:email>')
def get_user_route(email : str):
    user_info = get_user(email)
    return {"status" : 404, "data" : None} if user_info is None else {"status" : 200, "data" : user_info}
