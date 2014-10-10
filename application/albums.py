from application import app, models
from flask import request, jsonify
#import models
s = models.s

@app.route("/albums", methods=["GET", "POST"])
def all_albums():
    if request.method == "GET":
        albums = s.query(models.Album).all()
        return jsonify({"albums": [k.json() for k in albums]})

    if request.method == "POST":
        data = request.json
        #print request.json
        temp = models.Album(name=data['name'],
                            description=data['description'])
        s.add(temp)
        s.commit()
        return jsonify({"albumid":  temp.id})

@app.route("/edit_album", methods=["POST"])
def edit_album():
    print request.form
    try:
        albumid = int(request.form['pk'])
        album = models.get_album(albumid)
        if request.form['name'] == "name":
            album.name = request.form['value']
        if request.form['name'] == "description":
            album.description = request.form['value']
        s.add(album)
        s.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error",
                        "msg": str(e)})

@app.route("/albums/<int:albumid>", methods=["GET", "PUT", "DELETE"])
def single_album(albumid):
    results = s.query(models.Album).filter(models.Album.id==albumid)
    if results.count() > 0:
        album = results[0]

        if request.method == "GET":
            return jsonify({"data": album.json()})

        elif request.method == "PUT":
            if "description" in request.json:
                album.description = request.json['description']
            if "name" in request.json:
                album.name = request.json['name']
            s.add(album)
            s.commit()
            return jsonify({"data": album.json()})

        elif request.method == "DELETE":
            s.delete(album)
            s.commit()
            return jsonify({"data": None})
    else:
        return jsonify({"data": None})


@app.route("/albums/<int:albumid>/tags",
           methods=["GET"])
def get_album_tags(albumid):
    """Get the tags associated with the album"""
    album = models.get_album(albumid)
    tags = []
    for photo in album.photos:
        for tag in photo.tags:
            if tag.user.id not in tags:
                tags.append(tag.user.id)
    return jsonify({"tags": tags})
