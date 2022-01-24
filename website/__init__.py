from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Configure Database - SQLALchemy
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    """ Create Flask App
    Appname = app
    """

    app = Flask(__name__)

    # Database Configuration
    app.config['SECRET_KEY'] = "SUPERSECRET"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Load Views Routes
    from .views import views
    app.register_blueprint(views, url_prefix="/")

    # Load Auth Routes
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")

    # Load DB Models
    from .models import User

    # Create DB
    create_database(app)

    return app

def create_database(app):
    """ Create a new database in the main website folder if 
        none was found.
    """
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Database created.")