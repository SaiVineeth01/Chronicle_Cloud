from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def home():
    # If the user is logged in, redirect them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))  # Redirect to dashboard
    # If not logged in, show the home page with login/signup options
    return render_template('home.html')

@home_bp.route('/dashboard')
@login_required
def dashboard():
    # Render the dashboard only if the user is logged in
    return render_template('dashboard.html', user=current_user)
