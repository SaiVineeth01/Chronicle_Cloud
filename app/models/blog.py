from app import db
from datetime import datetime

class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    
    notifications = db.relationship('Notification', back_populates='blog', cascade='all, delete', passive_deletes=True)  # ✅ Add this

    
    user = db.relationship('User', back_populates='blogs')  # ✅ Changed from 'author'

    

    def __repr__(self):
        return f"<Blog {self.title}>"
