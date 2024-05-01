from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Flask Birdhouse Tracking app for Audubon Miami Valley
# Author: Gregory Spain
# Date: May 10, 2023


# initialize SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # replace inside the <> with your information
    app.config['SECRET_KEY'] = 'Your Key Here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Your Connection String'

    db.init_app(app)

    # initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

