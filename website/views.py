""" Views Blueprint
    ---------------------------
    Simple Flask Blog WebApp
    Developped by: Luiz Marin
"""

from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from .models import User
from .models import Post
from .models import Comment
from .models import Like
from . import db

views = Blueprint("views", __name__)


# Home Page Route
@views.route("/")
@views.route("/home")
@login_required
def home():
    """ Home Page Route

        Parameters  :   None

        Redirect to :   Home Page
    """

    posts = Post.query.all()
    return render_template('home.html.j2', user=current_user, posts=posts)


# Create Post Route
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    """ Create Post Route

        Parameters  :   None
        
        Methods     :   GET, POST

        Redirect to :   Main page when successfull
    """

    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            flash("Your post should not be empty!", category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post Created!", 'success')
            return redirect(url_for('views.home'))

    return render_template('create-post.html.j2', user = current_user)


# Delete Post Route
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    """ Delete Post Route

        Parameters  :   post id
        
        Methods     :   None

        Redirect to :   Main page when successfull
    """

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
@views.route("/like-post/<post_id>", methods=['GET'])
@login_required
def like_post(post_id):
    """ Like Post Route

        Parameters  :   post id
        
        Methods     :   GET

        Redirect to :   Main page when successfull
    """

    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

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


# View User's Posts
@views.route("/posts/<username>")
@login_required
def view_posts(username):
    """ View User Posts Route

        Parameters  :   username
        
        Methods     :   None

        Redirect to :   Main page when successfull
    """

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("User not found!", category='error')
        return redirect(url_for('views.home'))
    else:
        return render_template("posts.html.j2", user=current_user, posts=user.posts, username=username)


# Create Comment Route
@views.route("/create-comment/<post_id>", methods=['GET', 'POST'])
@login_required
def create_comment(post_id):
    """ Create Comment Route

        Parameters  :   post id
        
        Methods     :   GET, POST

        Redirect to :   Main page when successfull
    """
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            flash("Your comment should not be empty!", category='error')
        else:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment created!", 'success')
            return redirect(url_for('views.home'))

    return render_template('create-comment.html.j2', user = current_user)


# Delete Comment Route
@views.route("/delete-comment/<id>")
@login_required
def delete_comment(id):
    """ Delete Comment Route

        Parameters  :   comment id
        
        Methods     :   None

        Redirect to :   Main page when successfull
    """
    comment = Comment.query.filter_by(id=id).first()

    if not comment:
        # Commento not found by the id provided
        flash("Comment does not exist!", category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        # User is not the author of the comment neither is the author of the post
        # Author of the post is able to delete comments
        flash("You don\'t have permission to delete this post!", category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted!")

    return redirect(url_for('views.home'))