from application import app, models
from flask import render_template, request
s = models.s


@app.route("/albums/<int:albumid>/photos/<int:photoid>/location/html")
def edit_location(albumid, photoid):
    photo = models.get_photo(photoid)
    return render_template("location.html",
                            photo=photo)


@app.route("/locations/html")
def show_locations():
    return render_template("edit_locations.html",
                           locations=s.query(models.Location).all())