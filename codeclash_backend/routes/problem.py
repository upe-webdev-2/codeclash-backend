import random
from typing import Union

from flask import Blueprint

import json
import uuid
import hashlib
import os

from codeclash_backend import prisma

problem = Blueprint('problem', __name__)

def specific_problem(id : str) -> Union[dict, None]:
    r"""
    Finds specific problem based on id passed into the route.

    Parameters
    ---------------
    id : str
        The index of the problem in the database needed to be returned to the user.
    
    Returns
    -------------
    Returns a dictionary containing the information of a problem.
    """
    
    data = prisma.problem.find_unique(
        where = {
            "id" : id
        }
    )
    
    if data is None:
        return None
    
    return data.dict()

def rand_problem() -> Union[dict, None]:
    r"""
    Finds random problem from the database of problems, which the users will answer.

    Returns
    -----------------
    Returns a dictionary containing the information of a problem.
    """
    problem_count = prisma.problem.count()
    
    if problem_count == 0:
        return None
    
    random_id = random.randint(0, problem_count - 1)

    problem = prisma.problem.find_unique(where = {
        "id" : str(random_id)
    })

    return problem.dict()

def is_valid_auth_token(token: str) -> bool:
    #Use this to generate new authorization tokens:
    #password = "mypassword" + os.environ.get("ACCESS_TOKEN_SALT")
    #hashed = hashlib.md5(password.encode()).hexdigest()
    #print(hashed)
    
    password = token + os.environ.get("ACCESS_TOKEN_SALT")
    hashed = hashlib.md5(password.encode()).hexdigest()
    return (hashed == os.environ.get("ACCESS_TOKEN"))

@problem.route('/<string:id>', methods = ["GET"])
def specific_problem_route(id : str):
    data = specific_problem(id)
    return {"status" : 404} if data is None else {"status" : 200, "data" : data}
    
@problem.route('/', methods = ["GET"])
def rand_problem_route():
    data = rand_problem()
    return {"status" : 404} if data is None else {"status" : 200, "data" : data}

@problem.route('/', methods = ["POST"])
def add_problem():
    post_body = request.json
    auth_token = request.headers.get("auth_token", None)
    
    if auth_token == None or not is_valid_auth_token(auth_token):
        return {"status": 401, "message": "Authorization token is not valid"}

    problem = post_body.get("problem", None)
    
    if problem == None:
        return {"status": 400, "message": "Request must contain a problem object"}
    
    try:
        problem = prisma.problem.create(data={
            "id": str(uuid.uuid1()), #probably a better way to generate the id. I thought postgres did this automatically?
            "title": problem["title"],
            "difficulty": enums.ProblemDifficulty[problem["difficulty"]],
            "objectives": problem["objectives"],
            "examples": [
                json.dumps(problem["examples"])
            ],
            "starterCode": problem["starterCode"],
            "testCases": [json.dumps(problem["testCases"])],
            "functionName": problem["functionName"]
        })
        
        return {"status": 200, "problem": problem}
    except:
        return {"status": 400, "message": "A type error occured when adding to the database"}  