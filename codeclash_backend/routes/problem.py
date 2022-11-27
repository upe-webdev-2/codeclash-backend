import random
from typing import Union

from flask import Blueprint, request
from prisma import enums, Json

import hashlib
import os

from codeclash_backend import prisma

problem = Blueprint('problem', __name__)

def specific_problem(id : int) -> Union[dict, None]:
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
            "problemNumber" : id
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
        return {
        "problemNumber" : 1,
        "id": "Two Sum",
        "title": "Two Sum",
        "difficulty": "Easy",
        "objectives": [
            "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "You may assume that each input would have exactly one solution, and you may not use the same element twice.",
            "You can return the answer in any order."
        ],
        "examples": [
            {
            "input": "nums = [2,7,11,15], target = 9",
            "output": "[0,1]",
            "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
            },
            {
            "input": "nums = [3,2,4], target = 6",
            "output": "[1,2]"
            },
            {
            "input": "nums = [3,3], target = 6",
            "output": "[0,1]"
            }
        ],
        "starterCode": 'def twoSum(nums: List[int], target: int) -> List[int]:\n\t# Code here...\n\tpass',
        "testCases": [{"inputs": [[2,7,11,15], 9], "output": [0,1]}, {"inputs": [[1,1,2,3,4,6,7], 8], "output": [2,5]}],
        "functionName": "twoSum"
        }
    
    random_id = random.randint(1, problem_count)

    problem = prisma.problem.find_unique(where = {
        "problemNumber" : random_id
    })

    return problem.dict()

def is_valid_auth_token(token: str) -> bool:
    # Use this to generate new authorization tokens:
    # password = "SPECIAL_PHRASE" + os.environ.get("ACCESS_TOKEN_SALT")
    # hashed = hashlib.md5(password.encode()).hexdigest()
    # print(hashed)

    password = token + os.environ.get("ACCESS_TOKEN_SALT")
    hashed = hashlib.md5(password.encode()).hexdigest()
    return (hashed == os.environ.get("ACCESS_TOKEN"))

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

        examples = [Json(example) for example in problem["examples"]]

        test_cases = [Json(test_case) for test_case in problem["testCases"]]

        problem = prisma.problem.create(data={
            "id": problem["id"],
            "title": problem["title"],
            "difficulty": enums.ProblemDifficulty[problem["difficulty"]],
            "objectives": problem["objectives"],
            "examples": examples,
            "starterCode": problem["starterCode"],
            "testCases": test_cases,
            "functionName": problem["functionName"]
        })
        
        return {"status": 200, "problem": problem.dict()}
    except Exception as e:
        print(e)
        return {"status": 400, "message": "A type error occured when adding to the database"}  