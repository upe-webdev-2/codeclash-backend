from flask import Blueprint
execute = Blueprint('execute', __name__)

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
    script += '\n\t\tassert(user_return == test_cases.get("output"))'

    return script

@execute.route('/')
def index():
    problem_example = {
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
        "starterCode": "def twoSum(nums: List[int], target: int) -> List[int]:\n\t# Code here...\n\tpass",
        "testCases": [{"inputs": [2], "output": 4}, {"inputs": [4], "output": 16}],
        "functionName": "solve"
    }

    string = append_script("def solve(num):\n\treturn num ** 2", problem_example)
    print(string)

    return {
        "script": string,
    }