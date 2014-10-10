import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, func
from sqlalchemy.dialects.sqlite import DATETIME, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

engine = create_engine('sqlite:///application/photon.db')
session = sessionmaker()
session.configure(bind=engine)
s = session()

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    vals = ["id", "name", "description"]
    def json(self):
        temp = {}
        for entry in self.vals:
            temp[entry] = getattr(self, entry)
        return temp

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    vals = ["id", "name", "description"]
    def json(self):
        temp = {}
        for entry in self.vals:
            temp[entry] = getattr(self, entry)
        return temp

class Album(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    vals = ["id", "name", "description"]
    def json(self):
        temp = {}
        for entry in self.vals:
            temp[entry] = getattr(self, entry)
        return temp

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    last_name = Column(Text)
    profile = Column(Text)
    vals = ["id",
            "first_name",
            "last_name",
            "profile"]
    #tag = relationship("Phototag", backref=backref("tags"))
    def json(self):
        temp = {}
        for entry in self.vals:
            temp[entry] = getattr(self, entry)
        return temp


        #"id":200,
        #"text":"John Doe",
        #"left":250,
        #"top":50,
        #"url": "person.php?id=200",
        #"isDeleteEnable": true

class Phototag(Base):
    __tablename__ = "phototags"
    id = Column(Integer, primary_key=True)
    text = Column(Text);
    x = Column(FLOAT)
    y = Column(FLOAT)
    url = Column(Text)
    delete_enabled = Column(Text)
    photo_id = Column(Integer, ForeignKey("photos.id"))
    photo = relationship("Photo", backref=backref("photo_tags"))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref=backref("users"))

    def json(self):
        temp = {}
        #temp['photoid'] = self.photo_id
        #temp['id'] = self.id
        temp['x'] = self.x
        temp['y'] = self.y
        temp['user_id'] = self.user_id
        #temp['url'] = self.url
        #temp['isDeleteEnable'] = self.delete_enabled
        temp['text'] = "%s %s" % (self.user.first_name,
                                  self.user.last_name)
        temp['id'] = self.id
        return temp

def get_user(userid=None, name=None):
    if userid:
        results = s.query(User).filter(User.id==userid)
    elif name:
        results = s.query(User).filter(User.name==name)
    if results.count() > 0:
        return results[0]
    else:
        raise Exception("Invalid user id %s" % userid)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    photo_id = Column(Integer, ForeignKey("photos.id"))
    #photo = relationship("Photo", backref=backref("comments"))
    user_id = Column(Integer, ForeignKey("users.id"))
    #user = relationship("User", backref=backref("comments"))

    def json(self):
        user = get_user(self.user_id)
        temp = {}
        temp['user'] = user.json()
        temp['id'] = self.id
        temp['text'] = self.text
        temp['photoid'] = self.photo_id
        temp['user'] = get_user(self.user_id).json()
        return temp


class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True)
    filename = Column(Text)
    caption = Column(Text)
    date = Column(DateTime)
    year = Column(Integer)

    #user_id = Column(Integer, ForeignKey('users.id'))
    #user = relationship(User, backref=backref('users', uselist=True, cascade="delete,all"))

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship(Event, backref = backref('events', uselist=True, cascade="delete,all"))

    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship(Location, backref = backref('locations', uselist=True, cascade="delete,all"))

    album_id = Column(Integer, ForeignKey('albums.id'))
    album = relationship(Album, backref = backref('photos', uselist=True, cascade="delete,all"))
    #users = relationship(User, backref = backref('users', uselist=True, cascade="delete,all"))
    def json(self):
        temp = {}
        temp["id"] = self.id
        temp['filename'] = self.filename
        temp['caption'] = self.caption
        temp['year'] = self.year
        temp['date'] = str(self.date)
        temp['month'] = self.date.month
        temp['day'] = self.date.day
        if self.event:
            temp["event"] = self.event.json()
        if self.location:
            temp["location"] = self.location.json()
        temp['album'] = self.album.json()
        if hasattr(self, "tags"):
            temp['tags'] = [k.json() for k in self.tags]
        return temp

def get_album(albumid):
    results = s.query(Album).filter(Album.id==albumid)
    if results.count() > 0:
        return results[0]
    else:
        raise Exception("Invalid album id %s" % albumid)

def get_photo(pid):
    results = s.query(Photo).filter(Photo.id==pid)
    if results.count() > 0:
        return results[0]
    else:
        raise Exception("Invalid photo id %s" % pid)

def get_user(userid=None, name=None):
    if userid:
        results = s.query(User).filter(User.id==userid)
    elif name:
        results = s.query(User).filter(User.name==name)
    if results.count() > 0:
        return results[0]
    else:
        raise Exception("Invalid user id %s" % userid)

def get_tag(tagid):
    results = s.query(Phototag).filter(Phototag.id==tagid)
    if results.count() > 0:
        return results[0]
    else:
        raise Exception("Invalid tag id %s" % tagid)

def get_event(eventid):
    results = s.query(Event).filter(Event.id==eventid)
    if results.count() > 0:
        return results[0]
    else:
        raise Exception("Invalid event id %s" % eventid)


def get_location(locationid):
    results = s.query(Location).filter(Location.id==locationid)
    if results.count() > 0:
        return results[0]
    else:
        raise Exception("Invalid location id %s" % locationid)

def get_comment(commentid):
    results = s.query(Comment).filter(Comment.id==commentid)
    if results.count() > 0:
        return results[0]
    else:
        raise Exception("Invalid comment id %s" % commentid)




def create():
    engine = create_engine('sqlite:///photon.db')
    Base.metadata.create_all(engine)
if __name__ == "__main__":
    engine = create_engine('sqlite:///photon.db')

    Base.metadata.create_all(engine)
    session = sessionmaker()
    session.configure(bind=engine)

    rezag = User(name="rezag")
    javad = User(name="javadg")

    album = Album(name="First Album", description="My very first album")

    koopmans = Location(name="Koopmans", description="Our home on Koopmans Ave, Santa Cruz")
    watertime = Event(name="Playing in the water")

    photo = Photo(filename="/Users/rjghassemi/Desktop/Dad.jpg",
                  caption="Dad and I",
                  date = datetime.datetime(1982,1,1),
                  #user = reza,
                  year = 1982,
                  event=watertime,
                  location = koopmans,
                  album=album)

    photo.tags.append(Tag(user=rezag))
    photo.tags.append(Tag(user=javad))
    #rezag.photos.append(photo)
    #first = Tag(user=rezag)
    #photo.users.append(rezag)

    s = session()
    s.add(rezag)
    #s.add(first)
    s.add(album)
    s.add(koopmans)
    s.add(watertime)
    s.add(photo)
    s.commit()
