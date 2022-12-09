from flask_login import UserMixin
from . import db

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    distance = db.Column(db.Float)
    moving_time = db.Column(db.Integer)
    elapsed_time = db.Column(db.Integer)
    start_date_local = db.Column(db.DateTime)
    manual_entry = db.Column(db.Boolean)
    average_speed = db.Column(db.Float)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    # Default is targeted at Seniors
    # https://bit.ly/3iUbOSW
    recommended_hours = db.Column(db.Integer)

    # The access token is what provides access to a specific Strava account
    strava_access_token = db.Column(db.String(100))
    # The refresh token is required to obtain a new access token
    strava_refresh_token = db.Column(db.String(100))
    # The number of seconds since Epoch when the current access token expires
    strava_expires_at = db.Column(db.Integer)
