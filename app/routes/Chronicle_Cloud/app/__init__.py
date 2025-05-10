from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from datetime import datetime
import logging

# Initialize extensions globally (without app)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Your login route name
migrate = Migrate()

def create_app():
    # Create Flask app
    app = Flask(
        __name__, 
        template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
        static_folder=os.path.join(os.path.dirname(__file__), 'static')
    )

    # Load environment variables from .env file
    load_dotenv()

    # App configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_default_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///../database/chroniclecloud.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

    # Optional: Add a custom Jinja filter (for date formatting)
    def format_date(value, format='%Y-%m-%d'):
        if isinstance(value, datetime):
            return value.strftime(format)
        return value
    app.jinja_env.filters['date'] = format_date

    # --- Register Blueprints ---
    from app.routes.auth_routes import auth_bp
    from app.routes.main_routes import main
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.content_routes import content_bp
    from app.routes.blog_routes import blog_bp
    from app.routes.home_routes import home_bp
    from app.routes.files_routes import files_bp
    from app.routes.search_routes import search_bp
    from app.routes.upload_routes import upload_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.notes_routes import notes_bp
    from app.routes.search_routes import search_bp
    from app.routes.notifications_routes import notifications_bp

    

    blueprints = [
        auth_bp, main, dashboard_bp, content_bp, blog_bp,
        home_bp, files_bp, search_bp, upload_bp, admin_bp, notes_bp,
    ]
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    for bp in blueprints:
        app.register_blueprint(bp)
        

    # Set up route for logging notes
    @app.route('/log_notes')
    def log_notes():
        from app.models import Note
        notes = Note.query.all()  # Fetch all notes
        for note in notes:
            app.logger.info(f"Note Title: {note.title}, Note Content: {note.content}")
        return "Check the logs for note details."

    return app

# Flask-Login user loader (to keep user session)
@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User  # Import inside to avoid circular imports
    return User.query.get(int(user_id))

# Make extensions available when importing
__all__ = ['create_app', 'db', 'migrate']
