from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager


csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
    login_manager.init_app(app)  # Initialize the login manager with the app
    app.config['SECRET_KEY'] = 'IAP-1-Master'  # Set the secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'test.db')  # Set the database URI

    csrf.init_app(app)  # Initialize CSRF protection with the app
    db.init_app(app)  # Initialize SQLAlchemy with the app

    with app.app_context():
        from .views import bp  # Import the blueprint inside the app context
        from .models import User
        app.register_blueprint(bp)

        @app.errorhandler(404)
        def error404(code):
            return render_template("error.html"), 404
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app