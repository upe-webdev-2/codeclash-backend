import os
import requests
from flask import Blueprint, request

array = [{
        "id": 1,
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
        "functionName": "twoSum",
        "testCases": [{
            "inputs": [[2,7,11,15], 9], 
            "output": [0,1]
        }, {
            "inputs": [[3,2,4], 6],
            "output": [1,2]
        }, {
            "inputs": [[3,3], 6],
            "output": [0,1]
        }]
    }]

execute = Blueprint('execute', __name__)

def append_script(script : str, problem_info : dict) -> str:
    """
    Returns a string appended with test cases, which would be run through the JDOODLE api.
    
    Paramaters
    -----------------
    script : str
        The initial code written by the user, represented as a string, obtained as a body parameter in the /execute route.
    problem_info : dict
        Information on problem being completed by the user, obtained through the /problem route (or access to database).
        The route number needed for this information can be obtained as a route parameter in the /execute call.
    
    Returns
    -----------------
    str
        A string containing the initial script passed by the user appended with test case code.

    """

    test_cases = problem_info.get("testCases")
    function_name = problem_info.get("functionName")
    input_length = len(test_cases[0].get("inputs"))

    script += f"""\ntest_cases = {test_cases}"""
    script += f"""\nif __name__ == "__main__":
        for case in test_cases:
            user_return = {function_name}(*case.get("inputs"))
            input_details = ""
            if user_return != case.get("output"):
                print("Inputs:")
                print(*case.get("inputs"))
                print("Your Output")
                print(user_return)
                print("Expected Output")
                print(case.get("output"))
                break
            """

    return script

@execute.route('/<id>', methods = ["POST"])
def index(id):
    """
    Returns the result of executing the user's code through the JDOODLE api. Before being run, the user code is appended by the append_script function.

    Parameters
    --------------
    id: int
        An integer representing the id of a the problem the user is solving. Used to query the database of problems for the append_script function.
    """
    post_body = request.json
    script = post_body.get("script")
    language = post_body.get("language")

    problem_info = array[int(id)]
    processed_script = append_script(script, problem_info)

    res = {}

    if request.method == "POST":
        url = "https://api.jdoodle.com/v1/execute"
        headers = {"Content-type" : "application/json"}
        data = {
            "clientId": os.environ.get("CLIENT_ID"),
            "clientSecret": os.environ.get("CLIENT_SECRET"),
            "script": processed_script,
            "language": language,
            "versionIndex": "0"
        }
        res = requests.post(url, json = data, headers = headers)

        res = res.json()

    else:
        res["status"] = 405
        res["message"] = "Please use POST method for route"
    return res