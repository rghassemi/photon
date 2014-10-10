from application import app, models
from flask import render_template, request
s = models.s

@app.route("/albums/<int:albumid>/photos/<int:photoid>/html")
def view_single_photo(albumid,photoid):
    photo = models.get_photo(photoid)
    comments = s.query(models.Comment).filter(models.Comment.photo_id == photoid)
    comments = [k.json() for k in comments]
    return render_template("view_photo.html",
                          photo=photo,
                          comments=comments)


@app.route("/albums/<int:albumid>/photos/<int:photoid>/tags/html")
def show_photo_tags(albumid, photoid):
    photo = models.get_photo(photoid)

    return render_template('edit_tags.html',
                           photo=photo)


@app.route("/albums/<int:albumid>/photos/html")
def show_photos(albumid):
    album = models.get_album(albumid)
    locations = []
    events = []
    for photo in album.photos:
        if photo.location not in locations:
            locations.append(photo.location)
        if photo.event:
            if photo.event not in events:
                events.append(photo.event)
    return render_template("album.html",
                           album=album,
                           locations=locations,
                           events=events)


@app.route("/albums/<int:albumid>/photos/upload")
def photo_upload_file(albumid):
    return render_template("upload_photo.html",
                           albumid=albumid)
