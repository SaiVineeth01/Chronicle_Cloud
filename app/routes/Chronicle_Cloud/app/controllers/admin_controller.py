# app/controllers/admin_controller.py
from app.models import User
from flask import jsonify

# Get all users
def get_all_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

# Get all notes (for admin dashboard)
def get_all_notes():
    notes = Note.query.all()
    return jsonify([{'id': note.id, 'title': note.title, 'content': note.content} for note in notes])

# Get all blogs (for admin dashboard)
def get_all_blogs():
    blogs = Blog.query.all()
    return jsonify([{'id': blog.id, 'title': blog.title, 'content': blog.content} for blog in blogs])
