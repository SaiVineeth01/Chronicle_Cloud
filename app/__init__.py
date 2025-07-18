import eventlet
eventlet.monkey_patch()

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, user_logged_in, user_logged_out
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()

# Global extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
socketio = SocketIO(cors_allowed_origins="*")
login_manager = LoginManager()
migrate = Migrate()

# ✅ Global set to store currently online user IDs
online_users = set()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ✅ Read from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    db_url = os.getenv("DATABASE_URL")

    if not app.config['SECRET_KEY']:
        raise RuntimeError("❌ SECRET_KEY not set in .env")
    if not db_url:
        raise RuntimeError("❌ DATABASE_URL not set in .env")
    if "sslmode" not in db_url:
        db_url += "?sslmode=require"

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # 🔧 Initialize Flask extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    # ✅ Logging
    logging.basicConfig(level=logging.INFO)
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

    # ✅ Maintenance mode check
    from app.controllers.admin_controller import get_settings

    @app.before_request
    def check_maintenance_mode():
        settings = get_settings()
        if settings.maintenance_mode and not (request.endpoint and request.endpoint.startswith('admin.')):
            return render_template('maintenance.html'), 503

    # ✅ Update last seen on every request
    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated and hasattr(current_user, 'last_seen'):
            try:
                current_user.last_seen = datetime.utcnow()
                db.session.commit()
            except Exception as e:
                app.logger.warning(f"Could not update last_seen: {e}")

    # ✅ Register Blueprints
    from app.routes import (
        auth_routes, main_routes, dashboard_routes, content_routes, blog_routes,
        home_routes, files_routes, search_routes, upload_routes, admin_routes,
        notes_routes, notifications_routes, concept_routes, ai_routes,
        analyze_routes, testimonial_routes
    )

    all_blueprints = [
        auth_routes.auth_bp, main_routes.main, dashboard_routes.dashboard_bp,
        content_routes.content_bp, blog_routes.blog_bp, home_routes.home_bp,
        files_routes.files_bp, search_routes.search_bp, upload_routes.upload_bp,
        admin_routes.admin_bp, notes_routes.notes_bp, ai_routes.ai_routes,
        testimonial_routes.testimonial_bp, analyze_routes.analyze_bp,
        analyze_routes.toxicity_bp, concept_routes.concept_bp,
    ]
    app.register_blueprint(notifications_routes.notifications_bp, url_prefix='/notifications')
    for bp in all_blueprints:
        app.register_blueprint(bp)

    # ✅ Jinja date formatting filter
    def format_date(value, format='%Y-%m-%d'):
        if isinstance(value, datetime):
            return value.strftime(format)
        return value
    app.jinja_env.filters['date'] = format_date

    # ✅ Inject global site settings into all templates
    @app.context_processor
    def inject_site_settings():
        from app.models import Settings
        return {'settings': Settings.query.first()}

    # ✅ Make online_users globally accessible
    app.online_users = online_users

    return app


# ✅ User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))


# ✅ Track login/logout to update online_users
@user_logged_in.connect
def when_user_logged_in(sender, user):
    online_users.add(user.id)
    print(f"✅ {user.username} logged in → ACTIVE")

@user_logged_out.connect
def when_user_logged_out(sender, user):
    if user and user.id in online_users:
        online_users.remove(user.id)
        print(f"🚫 {user.username} logged out → INACTIVE")


# ✅ SocketIO events (optional)
@socketio.on('connect')
def handle_connect():
    print('✅ SocketIO client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('🚫 SocketIO client disconnected')


# ✅ Exported symbols
__all__ = ['create_app', 'db', 'migrate']
