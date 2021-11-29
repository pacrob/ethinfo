# gotta run 'export FLASK_APP=hello? nope, not if it's named app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"