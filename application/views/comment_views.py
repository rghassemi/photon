from application import app, models
from flask import render_template, request
s = models.s


@app.route("/photos/<int:photoid>/comments/html")
def get_photo_comments(photoid):
    comments = s.query(models.Comment).filter(models.Comment.photo_id==photoid)
    comments = [k.json() for k in comments]
    return render_template("comments.html", photoid=photoid, comments=comments)