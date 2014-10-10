from application import app, models
from flask import render_template, request
s = models.s

@app.route("/albums/html")
def show_all_albums():
    albums = s.query(models.Album).all()
    return render_template("albums.html",
                           albums=albums)

@app.route("/albums/new")
def new_album():
    return render_template("new_album.html")