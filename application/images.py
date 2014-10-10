from application import app
from flask import jsonify, request, make_response, send_file
import models
import os
from PIL import Image
from models import s

def rotate(filename="/Users/rjghassemi/Desktop/Dad.jpg",
           angle=90):
    src = Image.open(filename)
    #(width, height) = src_im.size
    #size = 100, 100
    x=src.rotate(angle)

    x.save(filename)


@app.route("/albums/<int:albumid>/photos/<int:photoid>/file")
def get_photo_fullsize(albumid, photoid):
    photo = models.get_photo(photoid)
    return send_file(photo.filename)


@app.route("/albums/<int:albumid>/photos/<int:photoid>/rotate")
def rotate_file(albumid, photoid):
    photo = models.get_photo(photoid)
    fname = photo.filename.split('/')[-1].split('.')[0] +".thumb.jpg"
    medfname = photo.filename.split('/')[-1].split('.')[0] +".medium.jpg"

    thumbnail_dir = os.path.join(app.config['MEDIA_URL'],
                                 str(albumid),
                                 "thumbs")
    fname = os.path.join(thumbnail_dir, fname)
    medfname = os.path.join(thumbnail_dir, medfname)

    if 'angle' in request.args:
        angle = int(request.args['angle'])
        try:
            rotate(photo.filename, angle)
            rotate(fname, angle)
            rotate(medfname, angle)
            return jsonify({"status": True})
        except Exception as e:
            return jsonify({"status": False,
                            "message": str(e)})
    return jsonify({"status": False,
                    "message": "angle not specified"})


@app.route("/albums/<int:albumid>/photos/<int:photoid>/medium")
def get_photo_medium(albumid, photoid):
    photo = models.get_photo(photoid)
    fname = photo.filename.split('/')[-1].split('.')[0] +".medium.jpg"

    thumbnail_dir = os.path.join(app.config['MEDIA_URL'],
                                 str(albumid),
                                 "thumbs")

    thumbnail = os.path.join(thumbnail_dir, fname)

    if not os.path.exists(thumbnail_dir):
        os.mkdir(thumbnail_dir)

    if not os.path.exists(thumbnail):
        width = 480  #request.args.get('width', 120)
        height = 360  #request.args.get('height', 90)
        quality = 70  #request.args.get('height', 70)
        crop = False  #request.args.get('crop', False)
        img = Image.open(photo.filename)
        size = (800, 600)
        img.thumbnail(size)
        img.save(thumbnail, "JPEG")

    return send_file(thumbnail)


@app.route("/albums/<int:albumid>/photos/<int:photoid>/thumb")
def get_photo_thumb(albumid, photoid):
    print os.getcwd()
    photo = models.get_photo(photoid)
    fname = photo.filename.split('/')[-1].split('.')[0] +".thumb.jpg"

    thumbnail_dir = os.path.join(app.config['MEDIA_URL'],
                                 str(albumid),
                                 "thumbs")

    thumbnail = os.path.join(thumbnail_dir, fname)

    if not os.path.exists(thumbnail_dir):
        os.mkdir(thumbnail_dir)

    if not os.path.exists(thumbnail):
        width = 480  #request.args.get('width', 120)
        height = 360  #request.args.get('height', 90)
        quality = 70  #request.args.get('height', 70)
        crop = False  #request.args.get('crop', False)
        img = Image.open(photo.filename)
        size = (240, 180)
        img.thumbnail(size)
        img.save(thumbnail, "JPEG")

    return send_file(thumbnail)

