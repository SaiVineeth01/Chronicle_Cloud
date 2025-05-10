from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
from app import db
from app.models.user import User


main = Blueprint('main', __name__)



@main.route('/')
def home():
    users = User.query.all()  # Query the User model
    return render_template('home.html', users=users)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash("Invalid credentials", "danger")
    return render_template('login.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("Username already taken", "danger")
            return redirect(url_for('main.signup'))

        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful!", "success")
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@main.route('/dashboard')
@login_required
def dashboard():
    total_notes = 5
    total_blogs = 3
    recent_notes = [{'title': 'Note 1', 'created_at': '2025-04-28'}, {'title': 'Note 2', 'created_at': '2025-04-27'}]
    recent_blogs = [{'title': 'Blog 1', 'created_at': '2025-04-26'}, {'title': 'Blog 2', 'created_at': '2025-04-25'}]
    return render_template('dashboard.html', user=current_user, total_notes=total_notes, total_blogs=total_blogs,
                           recent_notes=recent_notes, recent_blogs=recent_blogs)

@main.route('/create_note', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        flash("Note created successfully!", "success")
        return redirect(url_for('main.dashboard'))
    return render_template('create_note.html')

@main.route('/notes')
@login_required
def notes():
    return render_template('notes.html')

@main.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    if request.method == 'POST':
        flash("Blog created successfully!", "success")
        return redirect(url_for('main.dashboard'))
    return render_template('create_blog.html')

@main.route('/blogs')
@login_required
def blogs():
    return render_template('blogs.html')

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            flash("File uploaded successfully!", "success")
    return render_template('upload.html')

@main.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')

@main.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('main.home'))
    return render_template('admin_dashboard.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
