from flask import Blueprint, render_template

documentation = Blueprint("documentation", __name__)

@documentation.route("/")
@documentation.route("/documentation")
def show_documentation():
    return render_template("documentation.html")