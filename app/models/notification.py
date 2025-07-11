from app import db
from datetime import datetime
import pytz
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql import func

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id', ondelete="CASCADE"), nullable=True)

    message = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False, default='info')

    created_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now())
    read = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='notifications')
    blog = db.relationship('Blog', back_populates='notifications')

    def to_dict(self):
        # Ensure created_at is timezone-aware
        utc = pytz.utc
        ist = pytz.timezone('Asia/Kolkata')

        utc_time = self.created_at
        if utc_time and utc_time.tzinfo is None:
            utc_time = utc.localize(utc_time)

        local_time = utc_time.astimezone(ist) if utc_time else None

        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'type': self.type,
            'created_at': local_time.strftime('%d-%m-%Y %I:%M %p') if local_time else None,
            'read': self.read
        }
