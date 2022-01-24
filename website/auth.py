""" Authentication Routes
    Everything related to User authentication and registration
"""
from flask import Blueprint, redirect, render_template, request, url_for, flash
from . import db
from .models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    """ Sign-up Route
    """

    if request.method  == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Verify if the user already exists in the DB and other validations
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash("This email is already in use!", category='error')
        elif username_exists:
            flash("This username is already in use!", category='error')
        elif len(username) < 4:
            flash("Username is too short, should have 4 or more characters!", category='error')
        elif len(password1) < 6:
            flash("Password is too short, should have 6 or more characters!", category='error')
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
        else:
            new_user = User(email=email, username=username, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("User created successfully!", category='success')

            return redirect(url_for('views.home'))

    return render_template('signup.html.j2', user=current_user)


# Login Route
@auth.route("/login", methods = ['GET', 'POST'])
def login():
    """ Login Route
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user exists, then check if the password matches
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password!", category='error')

    return render_template('login.html.j2', user=current_user)

# Logout Route
@auth.route("/logout")
@login_required
def logout():
    """
    Login Route
    Redirect the user to the url for views/home
    """
    logout_user()
    return redirect(url_for("views.home"))
