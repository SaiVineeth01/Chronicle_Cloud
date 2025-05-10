from functools import wraps
from flask import session, redirect, url_for, flash
from app.models.user_model import User
from app.utils.decorators import admin_required

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in as admin.')
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('You do not have permission to access this page.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
