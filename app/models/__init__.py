# app/models/__init__.py

from app import db
from .user import User
from .note import Note
from .file import File
from .blog import Blog

from .notification import Notification




# Set up cross-model relationships AFTER all models are imported

# This binds Blog to User after both classes are loaded
User.blogs = db.relationship('Blog', backref='author_blogs', lazy=True)
