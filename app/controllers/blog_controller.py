from app.models import db, Blog
from datetime import datetime

def save_blog(title, category, content, user_id):
    try:
        # Create a new Blog instance
        new_blog = Blog(
            title=title,
            category=category,
            content=content,
            created_at=datetime.utcnow(),
            user_id=user_id
        )

        db.session.add(new_blog)
        db.session.commit()

        return True
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return False
