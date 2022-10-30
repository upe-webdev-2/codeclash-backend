from array import array
import random
from flask import Blueprint

problem = Blueprint('problem', __name__)
#store problems in a dictionary
#return a random question 
#user could do /problem /1 that returs the problem at index 1 of the array
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
        "testCases": [{"inputs": [[2,7,11,15], 9], "output": 4}, {"inputs": [4], "output": 16}],
        "functionName": "twoSum"
    }, 
         {
        "id": 1,
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "objectives": [
            "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
            "An input string is valid if:",
            "1. Open brackets must be closed by the same type of brackets."
            "2. Open brackets must be closed in the correct order."
            "3. Every close bracket has a corresponding open bracket of the same type."
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
        "starterCode": 'def isValid(self, s): \n\t# Code here...\n\t',
        "testCases": [{"inputs": ["()"], "output": True}, {"inputs": ["(]"], "output": False}, {"inputs": ["()[]{}"], "output": True}],
        "functionName": "validParentheses"
        }, 
        {}]


@problem.route('/<int:id>')
def problem(id):
    if id >= len(array):
        return {'status':404, 'message':'invalid query parameter called id'}
    return array[id]
    
@problem.route('/')
def rand_problem():
    random_num = random.choice(array)
    return array[random_num]
    

        
   