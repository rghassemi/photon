from application import app
from flask import jsonify, request
import models
from models import s
import datetime
import os


@app.route("/albums/<int:albumid>/photos/<int:photoid>/location",
           methods=["GET", "POST", "DELETE"])
def single_photo_location(albumid, photoid):
    photo = models.get_photo(photoid)
    if request.method == "GET":
        location = None
        if photo.location:
            location = photo.location.json()
        return jsonify({"location": location})

    elif request.method == "POST":
        if 'location_id' in request.json:
            location = models.get_location(int(request.json['location_id']))
            photo.location = location
            s.add(photo)
            s.commit()
        else:
            location = models.Location(name=request.json['name'],
                                       description=request.json['description'])
            photo.location = location
            s.add(location)
            s.add(photo)
            s.commit()
        return jsonify({"location": photo.location.id})

    elif request.method == "DELETE":
        s.delete(photo.location)
        s.commit()
        return jsonify({"location": None})


@app.route("/locations")
def list_locations():
    locations = s.query(models.Location).all()
    return jsonify({"locations": [k.json() for k in locations]})



@app.route("/locations/<int:locationid>", methods=["GET", "PUT", "DELETE"])
def single_location(locationid):
    location = models.get_location(locationid)
    if request.method == "GET":
        return jsonify(location.json())
    elif request.method == "PUT":
        try:
            if 'name' in request.json:
                location.name = request.json['name']
            if 'description' in request.json:
                location.description = request.json['description']
            s.add(location)
            s.commit()
            return jsonify({"status": True})
        except Exception as e:
            return jsonfiy({"status": False,
                            "message": str(e)})
    elif request.method == "DELETE":
        try:
            s.delete(location)
            s.commit()
            return jsonify({"status": True})
        except Exception as e:
            return jsonify({"status": True,
                            "message": str(e)})