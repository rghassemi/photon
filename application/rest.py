from application import app
from flask import jsonify, request, make_response

import models

@app.route("/")
def home():
    return "Hello"
