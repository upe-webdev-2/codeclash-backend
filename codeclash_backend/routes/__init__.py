from codeclash_backend import app

from .problem import problem
from .execute import execute
from .user import user
from .documentation import documentation

app.register_blueprint(problem, url_prefix = '/problem')
app.register_blueprint(execute, url_prefix = '/execute')
app.register_blueprint(user, url_prefix = '/user')
app.register_blueprint(documentation, url_prefix = '/')