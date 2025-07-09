# app/routes/settings_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Settings, db

settings_bp = Blueprint('settings', __name__, url_prefix='/admin')

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    # Only allow admin users
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('main.dashboard'))

    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        db.session.add(settings)
        db.session.commit()

    if request.method == 'POST':
        settings.site_name = request.form['site_name']
        settings.theme = request.form['theme']
        settings.signup_enabled = request.form['signup_enabled'] == 'true'
        settings.maintenance_mode = request.form['maintenance_mode'] == 'true'
        settings.default_role = request.form['default_role']
        settings.email_notifications = request.form['email_notifications'] == 'true'
        
        db.session.commit()
        flash("Settings updated!", "success")
        return redirect(url_for('settings.settings'))

    return render_template('admin/settings.html', settings=settings)
