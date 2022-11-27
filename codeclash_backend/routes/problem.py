import random
from typing import Union

from flask import Blueprint

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
        return {
        "id": 0,
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
    
    random_id = random.randint(0, problem_count - 1)

    problem = prisma.problem.find_unique(where = {
        "id" : str(random_id)
    })

    return problem.dict()

@problem.route('/', methods = ["POST"])
def add_problem():
    return