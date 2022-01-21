from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging

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
    from .config import secret,db_uri
    #Create the PYODBC string for a MSSQL database
    

    #sqlalchemy database connection string and init of DB
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SECRET_KEY'] = secret

    db.init_app(app)

    #Flask login manager for handling user auth
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .src.db.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    """

    # Import blueprints for subsections of the page
    #Auth pages

    from .src.auth.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #Front page
    from .src.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #Cereal sub pages
    from .src.cereal import cereal as cereal_blueprint
    app.register_blueprint(cereal_blueprint)
    #API no pages
    from .src.api.api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    """



    return app