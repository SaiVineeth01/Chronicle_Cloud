from app import db
from datetime import datetime, timezone
from pytz import utc

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.String(255), nullable=True)

    # Store in UTC safely
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    uploaded_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id', name='fk_uploaded_by_user'),
        nullable=False
    )

    user = db.relationship('User', backref='uploaded_files')

    # ✅ Add reverse relationship to notifications
    notifications = db.relationship('Notification', back_populates='file', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<File {self.filename}>'
