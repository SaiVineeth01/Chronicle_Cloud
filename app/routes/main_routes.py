# app/routes/main_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
from app import db
from app.models.user import User
from app.models.testimonial import Testimonial
from app.models.activity import Activity
from app.models.blog import Blog
from pytz import timezone



main = Blueprint('main', __name__)


@main.route('/')
def home():
    users = User.query.all()
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
    # Get latest 3 blog posts
    blogs = Blog.query.order_by(Blog.created_at.desc()).limit(3).all()

    # Get all testimonials
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()

    # Get latest 5 activities
    activities = Activity.query.order_by(Activity.timestamp.desc()).limit(10).all()

    # Convert UTC timestamps to IST
    ist = timezone('Asia/Kolkata')
    for a in activities:
        if a.timestamp:
            a.timestamp = a.timestamp.replace(tzinfo=timezone('UTC')).astimezone(ist)

    # Optional dummy summary data
    total_notes = 5
    total_blogs = 3
    recent_notes = [
        {'title': 'Note 1', 'created_at': '2025-04-28'},
        {'title': 'Note 2', 'created_at': '2025-04-27'}
    ]
    recent_blogs = [
        {'title': 'Blog 1', 'created_at': '2025-04-26'},
        {'title': 'Blog 2', 'created_at': '2025-04-25'}
    ]

    return render_template(
        'dashboard.html',
        user=current_user,
        testimonials=testimonials,
        activities=activities,
        total_notes=total_notes,
        total_blogs=total_blogs,
        recent_notes=recent_notes,
        recent_blogs=recent_blogs,
        blogs=blogs
    )

@main.route('/submit_testimonial', methods=['POST'])
@login_required
def submit_testimonial():
    message = request.form.get('message')
    if message:
        testimonial = Testimonial(username=current_user.username, message=message)
        db.session.add(testimonial)
        db.session.commit()
        flash("Thank you for your feedback!", "success")
    else:
        flash("Testimonial cannot be empty.", "danger")
    return redirect(url_for('main.dashboard'))


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

@main.route('/contact')
def contact():
    return render_template('contact.html')