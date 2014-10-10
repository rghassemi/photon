from application import app
from flask import render_template
import album_views
import photo_views
import event_views
import location_views
import comment_views


@app.route("/test")
def test():
    return render_template("testpanel.html")