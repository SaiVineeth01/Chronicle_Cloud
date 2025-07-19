from datetime import datetime
from app import db

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50))
    due_date = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Relationship to User
    user = db.relationship('User', back_populates='notes')

    # ✅ Add reverse relationship to notifications
    notifications = db.relationship('Notification', back_populates='note', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Note {self.title}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
# ✅ Property for formatted created date
    @property
    def created_local(self):
        return self.created_at.strftime('%d-%m-%Y') if self.created_at else 'N/A'
