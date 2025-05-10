# app/routes/dashboard_routes.py

from flask import Blueprint, render_template

# Create a Blueprint for dashboard routes
dashboard_bp = Blueprint('dashboard', __name__)

# Dashboard route
@dashboard_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
