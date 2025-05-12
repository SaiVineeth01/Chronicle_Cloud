from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
import os
from datetime import datetime
import logging
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
socketio = SocketIO(cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
        static_folder=os.path.join(os.path.dirname(__file__), 'static')
    )

    # Load environment variables
    load_dotenv()

    # Use secrets from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_default_key')
    
    # Set SQLAlchemy to use SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Update with your desired path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.jinja_env.auto_reload = True
    app.jinja_env.cache = {}

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    from app.sockets import events  

    logging.basicConfig(level=logging.INFO)
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

    def format_date(value, format='%Y-%m-%d'):
        if isinstance(value, datetime):
            return value.strftime(format)
        return value
    app.jinja_env.filters['date'] = format_date

    from app.controllers.admin_controller import get_settings
    @app.before_request
    def check_maintenance_mode():
        settings = get_settings()
        if settings.maintenance_mode and not (request.endpoint and request.endpoint.startswith('admin.')): 
            return render_template('maintenance.html'), 503

    # Routes
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
    from app.routes.notifications_routes import notifications_bp

    blueprints = [
        auth_bp, main, dashboard_bp, content_bp, blog_bp,
        home_bp, files_bp, search_bp, upload_bp, admin_bp, notes_bp
    ]

    app.extensions['socketio'] = socketio
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    for bp in blueprints:
        app.register_blueprint(bp)

    @app.route('/log_notes')
    def log_notes():
        from app.models import Note
        notes = Note.query.all()
        for note in notes:
            app.logger.info(f"Note Title: {note.title}, Note Content: {note.content}")
        return "Check the logs for note details."

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))

@socketio.on('connect')
def handle_connect():
    print('✅ Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('🚫 Client disconnected')

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, use_reloader=True, host='0.0.0.0', port=5000)
