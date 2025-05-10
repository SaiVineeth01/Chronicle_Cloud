# models/content.py
from app import db

class Content(db.Model):
    __tablename__ = 'content'  # Table name in the database

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Content {self.title}>"
