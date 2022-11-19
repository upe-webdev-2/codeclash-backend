import os
import requests
from flask import Blueprint, request

from codeclash_backend import socketio
from .problem import specific_problem

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

def append_script(script : str, problem_info : dict, is_test = False) -> str:
    """
    Returns a string appended with test cases, which would be run through the JDOODLE api.
    
    Paramaters
    -----------------
    script : str
        The initial code written by the user, represented as a string, obtained as a body parameter in the /execute route.
    problem_info : dict
        Information on problem being completed by the user, obtained through the /problem route (or access to database).
        The route number needed for this information can be obtained as a route parameter in the /execute call.
    is_test : boolean
        Boolean determining whether the user is running only one test case or all test cases
    
    Returns
    -----------------
    str
        A string containing the initial script passed by the user appended with test case code.

    """
    test_cases = problem_info.get("testCases")

    if is_test:
        test_cases = test_cases[:1]

    function_name = problem_info.get("functionName")
    input_length = len(test_cases[0].get("inputs"))

    script += """\nprint("STARTING_TESTS")"""
    script += f"""\ntest_cases = {test_cases}"""
    script += f"""\nif __name__ == "__main__":
        for case in test_cases:
            user_return = {function_name}(*case.get("inputs"))
            input_details = ""
            print("TEST_RESULT")
            if user_return != case.get("output"):
                print("TEST_FAILED")
                print("Inputs:", end = " ")
                print(*case.get("inputs"))
                print("Expected Output", end = " ")
                print(case.get("output"))
                print("Your Output", end = " ")
                print(user_return)
            else:
                print("TEST_PASSED")
            """

    return script

def parse_output(res : dict, test_cases : dict, is_test = False):
    output = res.get("output")
    parsed_result = {**res}
    if output is None:
        return {"error" : "Something went wrong with JDOODLE"}
    
    if "STARTING_TESTS" not in output:
        return parsed_result
    
    output = output.split("STARTING_TESTS")[-1]
    
    test_results = []

    output = output.replace("\n", "")
    tests = output.split("TEST_RESULT")[1:]

    passed_all_cases = True

    for index, test in enumerate(tests):

        if "TEST_FAILED" not in test and "TEST_PASSED" not in test:
            continue

        test_info = {}
        if "TEST_FAILED" in test:
            passed_all_cases = False
            test_info["passed"] = False
            test_info["userOutput"] = test.split("Your Output")[-1]
        elif "TEST_PASSED" in test:
            test_info["passed"] = True
        
        test_info["input"] = test_cases[index].get("inputs")
        test_info["expectedOutput"] = test_cases[index].get("output")

        test_results.append(test_info)
    
    if not is_test:
        parsed_result["passedAllCases"] = passed_all_cases
    
    parsed_result["testResults"] = test_results
    return parsed_result

def execute_code(script : str, problem_id : int, is_test = False, language = "python3", version_index = "3") -> None:
    """
    Executes user code through the JDOODLE API and returns a dictionary of information based on
    the JDOODLE output.

    Parameters
    ---------------
    script : str
        A string of code written by the user
    
    problem_id : int
        The unique id of the problem being solved by the user, which indicates the test_cases that should be 
        appended to the script parameter.
    
    is_test : bool
        Boolean to determine whether user is only testing out code, in which case only the first test case will be ran.
    
    language : str
        Language that the user's code is written in, used in the JDOODLE compiler, linked here: https://docs.jdoodle.com/integrating-compiler-ide-to-your-application/languages-and-versions-supported-in-api-and-plugins
    
    version_index : str
        Integer representing version of language, as per JDOODLE's documentation, linked here: https://docs.jdoodle.com/integrating-compiler-ide-to-your-application/languages-and-versions-supported-in-api-and-plugins
    """

    problem_info = specific_problem(problem_id)
    processed_script = append_script(script, problem_info, is_test)

    res = {}

    url = "https://api.jdoodle.com/v1/execute"
    headers = {"Content-type" : "application/json"}
    data = {
        "clientId": os.environ.get("CLIENT_ID"),
        "clientSecret": os.environ.get("CLIENT_SECRET"),
        "script": processed_script,
        "language": language,
        "versionIndex": version_index
    }

    res = requests.post(url, json = data, headers = headers)

    res = res.json()

    return parse_output(res, problem_info.get("testCases"), is_test)

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

    code_output = execute_code(script, int(id))

    return code_output