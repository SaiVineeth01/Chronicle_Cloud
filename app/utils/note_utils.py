# app/utils/note_utils.py

from app.models.content import Content

def create_note(title, body):
    new_note = Content(title=title, body=body)
    db.session.add(new_note)
    db.session.commit()
    return new_note

def get_notes():
    return Content.query.all()
