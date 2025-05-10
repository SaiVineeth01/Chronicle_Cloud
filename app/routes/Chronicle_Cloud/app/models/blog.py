from app import db

class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Blog {self.title}>"

class Comment(db.Model):
    __tablename__ = 'comment'  # You might want to ensure this is 'comments' to follow naming conventions

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)  # Corrected foreign key
