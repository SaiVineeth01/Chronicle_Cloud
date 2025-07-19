from app.models import db, Note
from datetime import datetime

def create_note(title, category, due_date, content):
    try:
        # Create a new Note instance
        new_note = Note(
            title=title,
            category=category,
            due_date=datetime.strptime(due_date, '%d-%m-%Y') if due_date else None,
            content=content
        )
        
        # Add to the database and commit
        db.session.add(new_note)
        db.session.commit()
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return False
