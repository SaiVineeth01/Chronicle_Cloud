from app import db
from datetime import datetime
import pytz
from sqlalchemy.dialects.postgresql import TIMESTAMP

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False, default='info')

    
    created_at = db.Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    
    read = db.Column(db.Boolean, default=False)

    
    user = db.relationship('User', back_populates='notifications')

    def to_dict(self):
        
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'type': self.type,
            'created_at': self.created_at.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%d-%m-%Y %I:%M %p'),  
            'read': self.read
        }
