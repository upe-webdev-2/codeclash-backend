import os
import requests
from flask import Blueprint, request
from dotenv import load_dotenv

execute = Blueprint('execute', __name__)
load_dotenv()

def append_script(script : str, problem_info : dict) -> str:
    test_cases = problem_info.get("testCases")
    function_name = problem_info.get("functionName")
    input_length = len(test_cases[0].get("inputs"))

    script += f"\ntest_cases = {test_cases}\n"
    script += f'\nif __name__ == "__main__":\n\tfor case in test_cases:'

    user_output_string = f"\n\t\tuser_return = {function_name}("

    for i in range(input_length):
        user_output_string += f"case.inputs[{i}],"

    user_output_string = user_output_string[:-1]
    user_output_string += ")"

    script += user_output_string

    script += '\n\t\tinput_details = ""'
    script += '\n\t\tinput_details += '
    script += r'f"\n{input}" for input in case["inputs"]'

    script += '\n\t\tassert user_return == test_cases.get("output")'
    script += r',f"Your Input: {input_details}\nYour Output: {user_return}\nExpected Output: {test_cases.get("output")}"'

    return script

@execute.route('/<id>', methods = ["POST", "GET"])
def index(id):
    
    post_body = request.json

    script = post_body.script
    language = post_body.language

    # IMPLEMENT GET PROBLEM INFO FROM ID

    res = {}

    if request.method == 'GET':
        url = "https://api.jdoodle.com/v1/execute"
        headers = {"Content-type" : "application/json"}
        data = {
            "clientId": os.environ.get("CLIENT_ID"),
            "clientSecret": os.environ.get("CLIENT_SECRET"),
            "script": script,
            "language": language,
            "versionIndex": "0"
        }
        res = requests.post(url, json = data, headers = headers)

        res = res.json()

    return res