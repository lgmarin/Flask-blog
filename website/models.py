""" Models for the DB structure
"""
from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships based on the User Model
    posts = db.relationship('Post', backref="user", passive_deletes = True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable = False)