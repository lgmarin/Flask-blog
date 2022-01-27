""" Models for the DB structure
    ---------------------------
    Simple Flask Blog WebApp
    Developped by: Luiz Marin
"""
from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    """ User Model

        Columns:

            id              :   Integer
            email           :   String
            username        :   String
            password        :   String
            date_created    :   DateTime

        Relatiosnhips:

            posts           :   Post Model
            comments        :   Comment Model
            likes           :   Like Model
    """

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    # Relationships based on the User Model
    posts = db.relationship('Post', backref="user", passive_deletes = True)
    comments = db.relationship('Comment', backref="user", passive_deletes = True)
    likes = db.relationship('Like', backref="user", passive_deletes = True)


class Post(db.Model):
    """ Post Model

        Columns:

            id              :   Integer
            text            :   Text
            date_created    :   DateTime
            author          :   Integer            

        Relatiosnhips:

            comments        :   Comment Model
            likes           :   Like Model
    """

    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable = False)

    # Relationships for Post Model
    comments = db.relationship('Comment', backref="post", passive_deletes=True)
    likes = db.relationship('Like', backref="post", passive_deletes=True)


class Comment(db.Model):
    """ Comment Model

        Columns:

            id              :   Integer
            text            :   Text
            date_created    :   DateTime
            author          :   Integer            
            post_id         :   Integer

    """

    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable = False)


class Like(db.Model):
    """ Like Model

        Columns:

            id              :   Integer
            date_created    :   DateTime
            author          :   Integer            
            post_id         :   Integer

    """

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,  default = datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)