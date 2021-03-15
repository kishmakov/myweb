import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    text = ">"

    for note in os.listdir("app/templates/notes"):
        text += " " + str(note)

    @app.route("/")
    def hello():
        return text

    return app


