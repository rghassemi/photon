from application import app
from flask import jsonify, request
import models
from models import s
import datetime


@app.route("/albums/<int:albumid>/photos/<int:photoid>/event",
           methods=["GET", "POST", "DELETE"])
def single_photo_events(albumid, photoid):


    photo = models.get_photo(photoid)
    if request.method == "GET":
        event = []
        if photo.event:
            event = [photo.event.json()]
        return jsonify({"event": event})

    elif request.method == "POST":
        print '###########'
        print request.json
        if 'event_id' in request.json:
            event = models.get_event(int(request.json['event_id']))
            photo.event = event
            #s.add(event)
            s.add(photo)
            s.commit()
        else:
            event = models.Event(name=request.json['name'],
                                 description=request.json['description'])
            photo.event = event
            s.add(event)
            s.add(photo)
            s.commit()


        return jsonify({'eventid': photo.event.id})

    elif request.method == "DELETE":
        s.delete(photo.event)
        s.commit()
        return jsonify({"event": None})


@app.route("/events")
def list_events():
    events = s.query(models.Event).all()
    return jsonify({"events": [k.json() for k in events]})


@app.route("/events/<int:eventid>", methods=["GET", "PUT", "DELETE"])
def single_event(eventid):
    event = models.get_event(eventid)
    if request.method == "GET":
        return jsonify(event.json())
    elif request.method == "PUT":
        try:
            if 'name' in request.json:
                event.name = request.json['name']
            if 'description' in request.json:
                event.description = request.json['event']
            s.add(event)
            s.commit()
            return jsonify({"status": True})
        except Exception as e:
            return jsonify({"status": False,
                            "message": str(e)})
    elif request.method == "DELETE":
        try:
            s.delete(event)
            s.commit()
            return jsonify({"status": True})
        except Exception as e:
            return jsonify({"status": True,
                            "message": str(e)})