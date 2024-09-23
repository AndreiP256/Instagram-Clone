from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import views
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # Daca schimbati baza de date, se schimba aici
    db = SQLAlchemy(app)

    from .backend.models import User  # Import your User model here
    db.init_app(app)

    app.register_blueprint(views.bp)

    return app
