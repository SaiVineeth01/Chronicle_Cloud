from app import db

# Import all models
from .user import User
from .note import Note
from .file import File
from .blog import Blog

from .notification import Notification
from .settings import Settings
from .subscriber import Subscriber
from .testimonial import Testimonial   # ✅ Include testimonial model
from .activity import Activity 

# Optional: Define cross-model relationships here if needed
# This is usually already handled inside individual model files,
# but if you're adding dynamically, it can go here.

# Example: If Blog.author is ForeignKey('users.id'), and not already set up:
# User.blogs = db.relationship('Blog', backref='author_blogs', lazy=True)
# But this is NOT needed if you have this in `blog.py` already
