from application import app, models
from flask import request, jsonify
#import models
s = models.s


@app.route("/photos/<int:photoid>/comments",
           methods=["GET", "POST"])
def photo_comments(photoid):
    if request.method == "GET":
        comments = s.query(models.Comment).filter(models.Comment.photo_id==photoid)
        comments = [k.json() for k in comments]
        return jsonify({"comments": comments})
    elif request.method == "POST":
        comment = models.Comment()
        comment.text = request.json['comment']
        comment.photo_id = photoid
        comment.user_id = 1
        s.add(comment)
        s.commit()
        return jsonify({"status": True})


@app.route("/photos/<int:photoid>/comments/<int:commentid>",
           methods=["GET", "PUT", "DELETE"])
def single_comment(photoid, commentid):
    if request.method == "DELETE":
        comment = models.get_comment(commentid)
        s.delete(comment)
        s.commit()
        return jsonify({"status": True})
