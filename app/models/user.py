from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(256), unique=True, nullable=False)
    email         = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role          = db.Column(db.String(20), nullable=False, default='user')  # 'user' or 'admin'
    is_active = db.Column(db.Boolean, default=True)
    # Relationships
    notes = db.relationship(
        'Note',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    blogs = db.relationship(
        'Blog',
        back_populates='author',
        cascade='all, delete-orphan'
    )

    notifications = db.relationship(
        'Notification',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

