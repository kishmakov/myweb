#!/usr/bin/env python
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('welcome.html', static_url='//kishmakov.ru/static/')