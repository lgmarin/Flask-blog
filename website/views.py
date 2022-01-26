from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from .models import Post
from .models import Comment
from .models import Like
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
@login_required
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

# Delete Post Route
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):

    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist!", category='error')
    elif current_user.id != post.author:
        flash("You don\'t have permission to delete this post!", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted!")

    return redirect(url_for('views.home'))

# Like Post Route
@views.route("/like-post/<post_id>")
@login_required
def like_post(post_id):
    
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id)

    if not post:
        # No post found for the provided id
        flash("Post does not exist!", 'error')
    elif like:
        # Like already exists for this post by this author
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for('views.home'))