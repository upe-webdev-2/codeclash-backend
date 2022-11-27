import random
from typing import Union, TypedDict

from flask import Blueprint, request
from prisma import Json, enums

from codeclash_backend import prisma

problem = Blueprint('problem', __name__)

array = [{
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
        },{    
        "id": 1,
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "objectives": [
            "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
            "An input string is valid if:",
            "1. Open brackets must be closed by the same type of brackets.",
            "2. Open brackets must be closed in the correct order.",
            "3. Every close bracket has a corresponding open bracket of the same type.",
        ],
        "examples": [
            {
            "input": "s = ()",
            "output": "True",
            "explanation": "Because there is an open and closed parentheses."
            },
            {
            "input": "s = ()[]{}",
            "output": "True"
            },
            {
            "input": "s = (]",
            "output": "False"
            }
        ],
        "starterCode": 'def isValid(s : str) -> bool: \n\t# Code here...\n\t',
        "testCases": [{"inputs": ["()"], "output": True}, {"inputs": ["(]"], "output": False}, {"inputs": ["()[]{}"], "output": True}],
        "functionName": "validParentheses"
        },{
        "id": 2,
        "title": "Roman to Integer",
        "difficulty": "Easy",
        "objectives": [
        "Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.",
        "Symbol\tValue",
        "I\t1",
        "V\t5",
        "X\t10",
        "L\t50",
        "C\t100",
        "D\t500",
        "M\t1000",
        "For example, 2 is written as II in Roman numeral, just two ones added together. 12 is written as XII, which is simply X + II.",
        "The number 27 is written as XXVII, which is XX + V + II.",
        "Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII.",
        "Instead, the number four is written as IV. Because the one is before the five we subtract it making four.",
        "The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:",
        "I can be placed before V (5) and X (10) to make 4 and 9.",
        "X can be placed before L (50) and C (100) to make 40 and 90.",
        "C can be placed before D (500) and M (1000) to make 400 and 900.",
        "Given a roman numeral, convert it to an integer.",
        ],
        "examples": [{
            "input": "s = III",
            "output": "3",
            "explanation": "III = 3"
            },{
            "input": "s = LVIII",
            "output": "58",
            "explanation": "L = 50, V= 5, III = 3"
            },{
            "input": "s = MCMXCIV",
            "output": "1994",
            "explanation": "M = 1000, CM = 900, XC = 90 and IV = 4"
            }],
        "starterCode": 'def romanToInt(s: str) -> int:\n\t# Code here...\n\t',
        "testCases": [{"inputs": ["III"], "output": 3}, {"inputs": ["LVIII"], "output": 58}, {"inputs": ["MCMXCIV"], "output": 1994}],
        "functionName": "romanToInt"
        }]

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
    return