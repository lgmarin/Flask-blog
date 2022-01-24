from crypt import methods
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from .models import User
from .models import Post
from . import db

views = Blueprint("views", __name__)

""" Define the routes for the webapp
"""

# Home Page Route
@views.route("/")
@views.route("/home")
@login_required
def home():

    posts = Post.query.all()
    return render_template('home.html.j2', user=current_user, posts=posts)

# Create Post Route
@views.route("/create-post", methods=['GET', 'POST'])
def create_post():

    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            flash("Your post should not be empty!", category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post Created!")
            return redirect(url_for('views.home'))

    return render_template('create-post.html.j2', user = current_user)