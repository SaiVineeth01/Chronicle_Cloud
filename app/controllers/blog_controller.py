from app.models import db, Blog
from datetime import datetime
from app.utils.text_image_generator import generate_blog_image_helper as generate_blog_image

def save_blog(title, category, content, user_id, ai_image=None):
    try:
        image_path = ai_image if ai_image else generate_blog_image(title, content)
        new_blog = Blog(
            title=title,
            category=category,
            content=content,
            image_url=image_path,
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
