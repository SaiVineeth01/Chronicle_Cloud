from datetime import datetime, timezone
from app.extensions import db  # Import db from extensions.py
from werkzeug.security import generate_password_hash, check_password_hash

# User model for storing user information
class User(db.Model):
    __tablename__ = 'user'


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationships
    notes = db.relationship(
        'Note',
        back_populates='user',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy='dynamic'
    )
    blogs = db.relationship(
        'Blog',
        back_populates='user',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy='dynamic'
    )
    files = db.relationship(
        'File',
        back_populates='user',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hashes and stores the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the password against the stored hash."""
        return check_password_hash(self.password_hash, password)


# Note model for storing notes
class Note(db.Model):
    __tablename__ = 'note'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=False, index=True)
    category = db.Column(db.String(100), index=True)
    tags = db.Column(db.String(200))
    due_date = db.Column(db.Date)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='published')  # published/draft
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationship
    user = db.relationship('User', back_populates='notes')

    def __repr__(self):
        return f'<Note {self.title}>'


# Blog model for storing blogs
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('blogs', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Blog {self.title}>"


# File model for storing uploaded files
class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    filename = db.Column(db.String(120), nullable=False)
    filepath = db.Column(db.String(300), nullable=False)  # Full path to the stored file
    uploaded_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship
    user = db.relationship('User', back_populates='files')

    def __repr__(self):
        return f'<File {self.filename}>'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
    user = db.Column(db.String(100))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

