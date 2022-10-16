from codeclash_backend import app
from flask import Flask, redirect, url_for, request

from codeclash_backend.routes.problem import problem
from codeclash_backend.routes.execute import execute

app.register_blueprint(problem, url_prefix = '/problem')
app.register_blueprint(execute, url_prefix = '/execute')