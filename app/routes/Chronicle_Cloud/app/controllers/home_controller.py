from flask import render_template, redirect, url_for, flash
from app import app
from app.models import User, Note, Blog
from app.controllers.auth_controller import login_required

@app.route('/dashboard')
@login_required  # Ensure the user is logged in
def dashboard():
    # Get the current user
    user = User.query.get_or_404(1)  # Replace with dynamic user retrieval
    total_notes = Note.query.filter_by(user_id=user.id).count()
    total_blogs = Blog.query.filter_by(user_id=user.id).count()

    # Fetch recent notes and blogs for the dashboard
    recent_notes = Note.query.filter_by(user_id=user.id).order_by(Note.created_at.desc()).limit(5).all()
    recent_blogs = Blog.query.filter_by(user_id=user.id).order_by(Blog.created_at.desc()).limit(5).all()

    # Render the dashboard template with dynamic content
    return render_template('dashboard.html', user=user, total_notes=total_notes, total_blogs=total_blogs,
                           recent_notes=recent_notes, recent_blogs=recent_blogs)

