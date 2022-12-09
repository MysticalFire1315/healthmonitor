from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import os

# Setup logging
from . import log

# Initialise SQLAlchemy to use later in models
db = SQLAlchemy()

# Database must first be configured. Follow instructions below:
# 
#   $ from healthmonitor_app import db, create_app
#   $ db.create_all(app=create_app())
# 
# More information at: https://do.co/374zVsv

# Use "Application Factory" style to set up app. More info in Flask docs:
# https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/
def create_app(config_filename="app_config.toml"):
    """
    Creates an app
    """

    app = Flask(__name__)

    # Use Flask-Appconfig to configure application
    AppConfig(app, config_filename)

    # Initialise Bootstrap connection
    # Note that this app uses Bootstrap-Flask, *NOT* Flask-Bootstrap. More
    # info about Bootstrap-Flask can be accessed at:
    # https://bootstrap-flask.readthedocs.io/en/stable/index.html
    Bootstrap(app)

    # Initialise SQLAlchemy connection
    db.init_app(app)

    # Initialise Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth_blueprint.login'
    login_manager.not_login_view = 'user_blueprint.dashboard'
    login_manager.init_app(app)

    # Specify user loader for Flask-Login
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table,
        # user it in the query for the user
        return User.query.get(int(user_id))

    # Register blueprints (used with application factory)

    # Blueprint for main routes in app
    from .routes_main import main_blueprint
    app.register_blueprint(main_blueprint)

    # Blueprint for auth routes in app
    from .routes_auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprint for user routes in app
    from .routes_user import user_blueprint
    app.register_blueprint(user_blueprint)

    # Blueprint for strava routes in app
    from .routes_strava import strava_blueprint
    app.register_blueprint(strava_blueprint)

    return app

if __name__ == '__main__':
    import sys
    sys.path.append(os.path.dirname(__name__))
    create_app().run(debug=True)