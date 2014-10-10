from application import app, models
from flask import render_template, request
s = models.s


@app.route("/albums/<int:albumid>/photos/<int:photoid>/event/html")
def edit_event(albumid, photoid):
    photo = models.get_photo(photoid)
    return render_template("event.html",
                            photo=photo)


@app.route("/events/html")
def show_events():
    return render_template("edit_events.html",
                           events=s.query(models.Event).all())