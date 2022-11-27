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
        return None
    
    random_id = random.randint(0, problem_count - 1)

    problem = prisma.problem.find_unique(where = {
        "id" : str(random_id)
    })

    return problem.dict()

@problem.route('/', methods = ["POST"])
def add_problem():
    return