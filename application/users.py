from application import app, models
from flask import request, jsonify
#import models
s = models.s

@app.route("/users")
def get_all_tags():
    users = s.query(models.User).all()
    return jsonify({"users": [k.json() for k in users]})