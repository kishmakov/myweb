import os
from flask import Flask, render_template, redirect
from index import notes_records


def create_app():
    app = Flask(__name__)

    if os.getenv("FLASK_ENV") == "development":
        app.config.from_object("config.Dev")
    else:
        app.config.from_object("config.Prod")

    sorted_notes = sorted(notes_records, key=lambda record: record.id, reverse=True)
    tags = sorted(list(set([tag for record in notes_records for tag in record.tags])))

    @app.route("/")
    def welcome():
        return redirect("/list")

    @app.route("/list")
    def list_all():
        return render_template("list_all.html", notes=sorted_notes, tags=tags)

    @app.route("/list/<tag>")
    def list_tagged(tag):
        tagged_notes = filter(lambda n: tag in n.tags, sorted_notes)
        other_tags = filter(lambda t: t != tag, tags)
        return render_template("list_tagged.html", tag=tag, notes=tagged_notes, tags=other_tags)

    @app.route("/n/<note_id>")
    def note(note_id):
        return render_template("n/{0}.html".format(note_id))

    return app


