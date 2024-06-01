from utils import image_to_desc
from . import db


class Account(db.Model):
    __tablename__ = 'accounts'
    accname = db.Column(db.String(255), primary_key=True, nullable=False)

class Playlist(db.Model):
    __tablename__ = 'playlists'
    playlistID = db.Column(db.String(100), primary_key=True, nullable=False)
    accname = db.Column(db.String(255), nullable=False)
    pldate = db.Column(db.Date)
    prompt = db.Column(db.String(10000))
    image_url = db.Column(db.String(512))
