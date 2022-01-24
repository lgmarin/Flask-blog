from flask import Flask
from os import path


def create_app():
    """ Create Flask App
    Appname = app
    """

    app = Flask(__name__)

    # Load Views
    from .views import views
    app.register_blueprint(views, url_prefix="/")


    return app
