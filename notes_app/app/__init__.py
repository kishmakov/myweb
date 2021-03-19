import os
from flask import Flask, render_template, redirect
from .index import notes_records


def create_app():
    app = Flask(__name__)

    if os.getenv("FLASK_ENV") == "development":
        app.config.from_object("config.Dev")
    else:
        app.config.from_object("config.Prod")

    @app.route("/")
    def index():
        return redirect("/list")

    @app.route("/list")
    def list_all():
        return render_template("list_all.html", notes=notes_records)

    @app.route("/list/<tag>")
    def list_tagged(tag):
        return render_template("list_tagged.html", notes=notes_records)

    @app.route("/n/<note_id>")
    def note(note_id):
        return render_template("n/{0}.html".format(note_id))

    return app


