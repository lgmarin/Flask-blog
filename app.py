""" Simple Flask Blog WebApp
    Developped by: Luiz Marin """
from flask import Flask, render_template, url_for

# Main App
app = Flask(__name__)


""" Define the routes for the webapp
"""
# Route for home page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# Route for sign up page
@app.route("/sign-up")
def signup():
    return render_template('signup.html')

# Route for login page
@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)