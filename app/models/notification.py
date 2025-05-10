# models/notification.py
from app import db
from datetime import datetime
import pytz

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False, default='info')
    
    # Using pytz to set time zone to IST (Indian Standard Time)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    
    read = db.Column(db.Boolean, default=False)
    
    # Relating notifications back to the User model
    user = db.relationship('User', back_populates='notifications')

    def to_dict(self):
        # Return the notification as a dictionary, including the formatted creation time
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'type': self.type,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Correct time format
            'read': self.read
        }
