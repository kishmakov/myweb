from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # for note in os.listdir("app/templates/notes"):

    static_url = '//kishmakov.ru/static/'

    @app.route("/")
    @app.route("/list/<tag>")
    def list(tag=None):
        return render_template("list.html", static_url=static_url)

    return app


