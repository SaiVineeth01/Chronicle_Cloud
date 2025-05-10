from flask import request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Login user function
def login_user_controller():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    
    # If the user exists and password is correct
    if user and check_password_hash(user.password, password):
        login_user(user)  # Log the user in
        flash('Logged in successfully!', 'success')
        return redirect(url_for('home.dashboard'))  # Redirect to the dashboard
    else:
        flash('Invalid credentials', 'danger')  # Invalid login credentials
        return redirect(url_for('auth.login'))  # Redirect back to the login page

# Signup user function
def signup_user_controller():
    email = request.form.get('email')
    username = request.form.get('username')  # Changed 'name' to 'username'
    password = request.form.get('password')

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('User already exists', 'warning')
        return redirect(url_for('auth.signup'))  # Redirect to signup page if user exists
    
    # Creating a new user with email, username, and hashed password
    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)  # Add the new user to the session
    db.session.commit()  # Commit the changes to the database
    flash('Account created successfully!', 'success')  # Show success message
    return redirect(url_for('auth.login'))  # Redirect to the login page after successful signup

# Logout user function
def logout_user_controller():
    logout_user()  # Log the user out
    flash('Logged out successfully!', 'info')  # Show logout success message
    return redirect(url_for('auth.login'))  # Redirect to login page after logout
