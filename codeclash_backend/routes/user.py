import asyncio
from codeclash_backend import prisma
from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/')
async def get_users():
    return "Users"