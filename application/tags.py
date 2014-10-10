from application import app, models
from flask import request, jsonify
#import models
s = models.s

@app.route("/photos/<int:photoid>/tags", methods=['GET', 'POST'])
def get_photo_tags(photoid):

    if request.method == "GET":
        tags = s.query(models.Phototag).filter(models.Phototag.photo_id == photoid)

        return jsonify({"tags": [k.json() for k in tags]})
    elif request.method == "POST":
        tag = models.Phototag()
        photo = models.get_photo(photoid)

        if request.json['type'] == "select":
            user = models.get_user(request.json['user'])

        else:
            user = models.User()
            user.first_name = request.json['first_name']
            user.last_name = request.json['last_name']

        tag.user = user
        tag.x = request.json['x']
        tag.y = request.json['y']

        tag.photo = photo
        s.add(tag)
        s.add(user)
        s.add(photo)
        s.commit()
        return jsonify({"status": True})


@app.route("/albums/<int:albumid>/photos/<int:photoid>/tags",
          methods=["GET", "POST"])
def photo_tags(albumid, photoid):
    photo = models.get_photo(photoid)
    tags = []
    if request.method == "GET":
        if photo.tags:

            for tag in photo.tags:
                if tag not in tags:
                    tags.append(tag.json())
        return jsonify({"tags": tags})

    elif request.method == "POST":
        if "userid" in request.json:
            user = get_user(request.json['userid'])

        elif 'name' in request.json:
            try:
                user = get_user(name=request.json['name'])
            except:
                user = models.User(name=request.json['name'])
            s.add(user)
            s.commit()

        else:
            raise Exception("No User specified")

        for tag in photo.tags:
            if tag.user.id == user.id:
                raise Exception("User already tagged")
        tag = models.Tag(user=user)
        photo.tags.append(tag)
        s.add(tag)
        s.add(photo)
        s.commit()
        return jsonify({"tag": tag.id})

    elif request.method == "GET":
        return jsonify({"tags": [k.json() for k in photo.tags]})


@app.route("/albums/<int:albumid>/photos/<int:photoid>/tags/<int:tagid>",
           methods=["GET", "DELETE"])
def single_tag(albumid, photoid, tagid):
    tag = models.get_tag(tagid)
    if request.method == "GET":
        
        return jsonify(tag.json())

    elif request.method == "DELETE":
        s.delete(tag)
        s.commit()
        return jsonify({"state": True})