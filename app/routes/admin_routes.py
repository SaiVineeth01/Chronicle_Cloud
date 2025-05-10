from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User, Note, Blog,db  # 👈 make sure Blog is imported
from app import db
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
from app.controllers import admin_controller

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')  # ✅ Fixed __name__

# Route to display all users
@admin_bp.route('/users')
@login_required
def users():
    if not current_user.is_admin():
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('admin.admin_login'))
    users = User.query.all()
    return render_template('admin/users.html', users=users)

# Admin signup route
@admin_bp.route('/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            flash("Username or Email already exists. Please choose a different one.", 'danger')
            return redirect(url_for('admin.admin_signup'))

        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, email=email, password_hash=hashed_password, role='admin')

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Admin account created successfully!", 'success')
            return redirect(url_for('admin.admin_login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error occurred: {str(e)}", 'danger')
            return redirect(url_for('admin.admin_signup'))

    return render_template('admin/signup.html')

# Admin login route
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            if user.is_admin():
                flash('Admin login successful.', 'success')
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash('You are not an admin.', 'danger')
                return redirect(url_for('admin.admin_login'))
        else:
            flash('Login failed. Check your email and/or password.', 'danger')
            return render_template('admin/login.html')

    return render_template('admin/login.html')

# Admin dashboard route
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('admin.admin_login'))

    user_count = User.query.count()
    return render_template('admin/admin_dashboard.html', user_count=user_count)

@admin_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    if not current_user.is_admin():
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('admin.admin_login'))

    settings = admin_controller.get_settings()
    print(settings)
    return render_template('admin/settings.html', settings=settings)

# Save settings
@admin_bp.route('/settings', methods=['POST'])
@login_required
def update_settings():
    if not current_user.is_admin():
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('admin.admin_login'))

    form_data = request.form
    try:
        admin_controller.update_settings(form_data)
        flash('Settings updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating settings: {str(e)}', 'danger')

    return redirect(url_for('admin.settings'))

# Admin logout route
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.admin_login'))

# Route to edit a user
@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin():
        flash('Access denied: Admins only.', 'danger')
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
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin.users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error occurred: {str(e)}', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user_id))

    return render_template('admin/edit_user.html', user=user)

# Route to delete a user
@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin():
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('admin.admin_login'))

    user = User.query.get(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error occurred: {str(e)}', 'danger')

    return redirect(url_for('admin.users'))

@admin_bp.route('/analytics')
@login_required
def analytics():
    if not current_user.is_admin():
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('admin.admin_login'))

    # Query total notes
    total_notes = Note.query.count()

    # Query total blogs
    total_blogs = Blog.query.count()

    # Query active users (role='user')
    active_users = User.query.filter_by(role='user').count()

    # Query admin users (role='admin')
    total_admins = User.query.filter_by(role='admin').count()

    # Get blogs grouped by category
    blogs_by_category = db.session.query(
        Blog.category, db.func.count(Blog.id)
    ).group_by(Blog.category).all()

    # ✅ Get notes grouped by category
    notes_by_category = db.session.query(
        Note.category, db.func.count(Note.id)
    ).group_by(Note.category).all()

    # Get the most recent blog post
    recent_blog = Blog.query.order_by(Blog.created_at.desc()).first()

    # Get the most recent note (assuming you have a 'Note' model with 'created_at' field)
    recent_note = Note.query.order_by(Note.created_at.desc()).first()

    # Create a dictionary with all analytics data
    analytics_data = {
        "total_notes": total_notes,
        "total_blogs": total_blogs,
        "active_users": active_users,
        "total_admins": total_admins,
        "blogs_by_category": blogs_by_category,
        "notes_by_category": notes_by_category,  # ✅ new
        "recent_blog": recent_blog,
        "recent_note": recent_note  # Fixed this line
    }

    # Debugging
    print(f"Total Notes: {total_notes}, Active Users: {active_users}")
    print(f"Total Blogs: {total_blogs}, Total Admins: {total_admins}")
    print(f"Blogs by Category: {blogs_by_category}")
    print(f"Notes by Category: {notes_by_category}")
    print(f"Recent Blog: {recent_blog.title if recent_blog else 'No recent blog'}")
    print(f"Recent Note: {recent_note.title if recent_note else 'No recent note'}")

    return render_template('admin/analytics.html', data=analytics_data)

