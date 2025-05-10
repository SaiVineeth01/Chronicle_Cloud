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

    # Foreign key to link Note to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # ✅ Add this relationship:
    user = db.relationship('User', back_populates='notes')

    def __repr__(self):
        return f'<Note {self.title}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
