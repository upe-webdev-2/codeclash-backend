from codeclash_backend import prisma
from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/<str:email>')
def get_users(email):
    data = prisma.user.find_unique(
        where = {
            'email' : email
        }
    )

    if data is None:
        return {"status" : 404, data : None}

    return {"status" : 200, "data" : data.json()}