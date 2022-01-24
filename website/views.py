from flask import Blueprint, Flask, render_template, url_for

views = Blueprint("views", __name__)

""" Define the routes for the webapp
"""
# Route for home page
@views.route("/")
@views.route("/home")
def home():
    return render_template('home.html.j2')

@views.route("/create-post")
def create_post():
    return render_template('create-post.html.j2')