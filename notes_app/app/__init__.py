from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # for note in os.listdir("app/templates/notes"):

    @app.route("/")
    def hello():
        return render_template("base.html")

    return app


