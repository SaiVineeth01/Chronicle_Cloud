from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models import User, Note, Blog, Settings, Testimonial, Activity
from app import db
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ---------------- Admin Auth ----------------

@admin_bp.route('/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or Email already exists.", 'danger')
            return redirect(url_for('admin.admin_signup'))

        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, email=email, password_hash=hashed_password, role='admin')

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Admin account created!", 'success')
            return redirect(url_for('admin.admin_login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", 'danger')

    return render_template('admin/signup.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            if user.is_admin():
                flash('Welcome Admin!', 'success')
                return redirect(url_for('admin.admin_dashboard'))
            flash('You are not an admin.', 'danger')
            return redirect(url_for('admin.admin_login'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('admin.admin_login'))

# ---------------- Dashboard & Analytics ----------------

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        flash('Access denied.', 'danger')
        return redirect(url_for('admin.admin_login'))

    user_count = User.query.count()
    testimonial_count = Testimonial.query.count()
    recent_testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).limit(5).all()
    activity_count = Activity.query.count()
    recent_activities = Activity.query.order_by(Activity.timestamp.desc()).limit(5).all()

    return render_template('admin/admin_dashboard.html',
                           user_count=user_count,
                           testimonial_count=testimonial_count,
                           recent_testimonials=recent_testimonials,
                           activity_count=activity_count,
                           recent_activities=recent_activities)

@admin_bp.route('/analytics')
@login_required
def analytics():
    if not current_user.is_admin():
        flash('Access denied.', 'danger')
        return redirect(url_for('admin.admin_login'))

    total_notes = Note.query.count()
    total_blogs = Blog.query.count()
    active_users = User.query.filter_by(role='user').count()
    total_admins = User.query.filter_by(role='admin').count()

    blogs_by_category = db.session.query(Blog.category, db.func.count(Blog.id)).group_by(Blog.category).all()
    notes_by_category = db.session.query(Note.category, db.func.count(Note.id)).group_by(Note.category).all()

    recent_blog = Blog.query.order_by(Blog.created_at.desc()).first()
    recent_note = Note.query.order_by(Note.created_at.desc()).first()

    testimonial_count = Testimonial.query.count()
    activity_count = Activity.query.count()

    return render_template('admin/analytics.html', data={
        "total_notes": total_notes,
        "total_blogs": total_blogs,
        "active_users": active_users,
        "total_admins": total_admins,
        "blogs_by_category": blogs_by_category,
        "notes_by_category": notes_by_category,
        "recent_blog": recent_blog,
        "recent_note": recent_note,
        "testimonial_count": testimonial_count,
        "activity_count": activity_count
    })

# ---------------- Settings ----------------

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if not current_user.is_admin():
        flash('Access denied.', 'danger')
        return redirect(url_for('admin.admin_login'))

    settings = Settings.query.get(1)
    if not settings:
        settings = Settings(id=1)
        db.session.add(settings)
        db.session.commit()

    if request.method == 'POST':
        form = request.form
        try:
            settings.site_name = form.get('site_name')
            settings.theme = form.get('theme')
            settings.signup_enabled = form.get('signup_enabled') == 'true'
            settings.maintenance_mode = form.get('maintenance_mode') == 'true'
            settings.moderation_required = form.get('moderation_required') == 'true'
            settings.email_notifications = form.get('email_notifications') == 'true'
            settings.admin_email = form.get('admin_email')

            db.session.commit()
            flash('Settings updated!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Update failed: {str(e)}', 'danger')

        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html', settings=settings)

# ---------------- User Management ----------------

@admin_bp.route('/users')
@login_required
def users():
    if not current_user.is_admin():
        flash('Access denied.', 'danger')
        return redirect(url_for('admin.admin_login'))

    users = User.query.all()

    # Users active in last 30 seconds
    now = datetime.utcnow()
    threshold = now - timedelta(seconds=30)
    online_users = [user.id for user in users if user.last_seen and user.last_seen >= threshold]

    return render_template('admin/users.html', users=users, online_users=online_users)

@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin():
        flash('Access denied.', 'danger')
        return redirect(url_for('admin.admin_login'))

    user = User.query.get(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        password = request.form['password']
        if password:
            user.password_hash = generate_password_hash(password, method='scrypt')

        try:
            db.session.commit()
            flash('User updated.', 'success')
            return redirect(url_for('admin.users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('admin/edit_user.html', user=user)

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin():
        flash('Access denied.', 'danger')
        return redirect(url_for('admin.admin_login'))

    user = User.query.get(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('admin.users'))

@admin_bp.route('/search_users')
@login_required
def search_users():
    if not current_user.is_admin():
        return '', 403

    q = request.args.get('q', '').strip()

    if q:
        users = User.query.filter(
            (User.username.ilike(f'%{q}%')) | (User.email.ilike(f'%{q}%'))
        ).all()
    else:
        users = User.query.all()

    now = datetime.utcnow()
    threshold = now - timedelta(seconds=30)
    online_users = [user.id for user in users if user.last_seen and user.last_seen >= threshold]

    return render_template('admin/_user_rows.html', users=users, online_users=online_users)
