from application import app
from flask import Flask, jsonify, request, make_response, render_template, send_from_directory, send_file
from werkzeug import secure_filename
from werkzeug.routing import BaseConverter


@app.route("/albums/<int:albumid>/photos/upload")
def photo_upload_file(albumid):
    return render_template("upload_photo.html",
                           albumid=albumid)

