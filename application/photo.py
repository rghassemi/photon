from application import app
from flask import jsonify, request
import models
from models import s
import datetime
import os


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'JPG', 'JPEG', "PNG"])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/edit_photo", methods=["POST"])
def edit_photo():
    print request.form
    try:
        photoid = int(request.form['pk'])
        photo = models.get_photo(photoid)
        if request.form['name'] == "caption":
            photo.caption = request.form['value']
        if request.form['name'] == "year":
            photo.year = int(request.form['value'])
        if request.form['name'] == 'date':
            #2002-03-03 00:00:00
            temp = request.form['value'].split('-')
            year = int(temp[0])
            month = int(temp[1])
            day = int(temp[2].split()[0])
            photo.date = datetime.datetime(year, month, day)
        s.add(photo)
        s.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error",
                        "msg": str(e)})



@app.route("/albums/<int:albumid>/photos/<int:photoid>/comments",
           methods=["GET", "POST"])
def all_comments(albumid, photoid):
    comments = s.query(models.Comment).filter(models.Comment.photo_id == photoid)
    temp = []
    return jsonify({"comments": [k.json() for k in comments]})


@app.route("/albums/<int:albumid>/photos/<int:photoid>",
           methods=["GET", "PUT", "DELETE"])
def single_photo(albumid, photoid):
    results = s.query(models.Photo).filter(models.Photo.id==photoid)
    if results.count() > 0:
        photo = results[0]
        if request.method == "GET":
            return jsonify(photo.json())

        elif request.method == "PUT":
            if 'caption' in request.json:
                photo.caption = request.json['caption']
            if 'date' in request.json:
                photo.date = request.json['date']
            if 'year' in request.json:
                photo.year = request.json['year']
                if 'month' in request.json and 'day' in request.json:
                    date = datetime.datetime(int(request.json['year']),
                                             int(request.json['month']),
                                             int(request.json['day']))
                    photo.date = date
            s.add(photo)
            s.commit()
            return jsonify(photo.json())
        elif request.method == "DELETE":
            if photo.tags:
                for item in photo.tags:
                    s.delete(item)
            s.delete(photo)
            s.commit()
            return jsonify({"photo": None})
    else:
        raise Exception("Invalid photid %s" % photoid)



@app.route("/albums/<int:albumid>/photos", methods=["GET", "POST"])
def album_photos(albumid):
    results = s.query(models.Album).filter(models.Album.id==albumid)

    if results.count() > 0:
        album = results[0]
        print album.id
        if request.method == "GET":
            temp = [k.json() for k in album.photos]
            return jsonify({"photos": temp})

        elif request.method == "POST":

            file = request.files['file']
            
            print file.filename
            if file and allowed_file(file.filename):
                photo = models.Photo()
                photo.album = album
                s.add(photo)
                s.commit()
                extension = file.filename.split('.')[-1]
                filename = "%s.%s" % (photo.id, extension)
                if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],
                                      str(albumid))):
                    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], str(albumid)))
                fullpath = os.path.join(app.config['UPLOAD_FOLDER'],
                                       str(albumid),
                                       filename)
                file.save(fullpath)
                photo.filename = fullpath

                s.add(photo)
                s.commit()
            return jsonify({"photoid": photo.id,
                                "albumid": albumid})