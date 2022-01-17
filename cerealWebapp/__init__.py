from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import urllib
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager
import os

"""
The entry point for the flask webapp, initializes the database connection, login manager and imports the blueprints.
The webpage is made up by using blueprints to define subsections. If futher expansion is required, 
add the blueprint as a seperate file and import them at the bottom of the create_app function where
the other blueprints are imported
"""

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static')
    from .config import secret,dbstring
    #Create the PYODBC string for a MSSQL database
    params = urllib.parse.quote_plus(dbstring)

    #sqlalchemy database connection string and init of DB
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
    app.config['SECRET_KEY'] = secret
    db.init_app(app)

    #Flask login manager for handling user auth
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))



    # Import blueprints for subsections of the page
    #Auth pages
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #Front page
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #Cereal sub pages
    from .cereal import cereal as cereal_blueprint
    app.register_blueprint(cereal_blueprint)

    #API no pages
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)



    app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
    )
    
    app.add_url_rule(
    "/list/<id>", endpoint="list_spec_cereal"
    )


    return app