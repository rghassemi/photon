from flask import Flask
from werkzeug.routing import BaseConverter
app = Flask(__name__)
import models as models
import os

UPLOAD_FOLDER = os.path.join(os.getcwd(),'application','photos')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MEDIA_FOLDER'] = UPLOAD_FOLDER
app.config['MEDIA_URL'] = UPLOAD_FOLDER
app.config['MEDIA_THUMBNAIL_URL'] = '/photos/thumbs'

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

import rest
import images
import albums
import views
import photo
import users
import tags
import events
import locations
import comments
