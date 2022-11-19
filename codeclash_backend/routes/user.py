from codeclash_backend import prisma
from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/<string:email>')
def get_users(email):
    data = prisma.user.find_first(where = {
        "email" : email
    })

    if data is None:
        return {"status" : 404}

    return {"status" : 200, "data" : data} # FIX: only include non-sensitive information
