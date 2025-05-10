from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Note
from datetime import datetime

# Define Blueprint
notes_bp = Blueprint('notes', __name__)

# Route to create a new note
@notes_bp.route('/create-note', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        due_date = request.form.get('due_date')
        content = request.form.get('content')

        # Validation for Title
        if not title:
            flash("Title is required!", "warning")
            return redirect(url_for('notes.create_note'))

        # Optional: Parse due date if provided
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                flash("Invalid due date format. Please use YYYY-MM-DD.", "warning")
                return redirect(url_for('notes.create_note'))

        # Ensure content is safe for rendering (strip extra spaces, you can add sanitization if needed)
        if content:
            content = content.strip()  # Remove extra spaces at the start/end

        # Create the new Note object
        new_note = Note(
            title=title,
            category=category,
            due_date=parsed_due_date,
            content=content,
            created_at=datetime.utcnow(),
            user_id=current_user.id
        )

        # Add to DB
        db.session.add(new_note)
        db.session.commit()

        flash("Note created successfully!", "success")
        return redirect(url_for('notes.view_notes'))

    return render_template('create_note.html')


# Route to display all notes for the logged-in user
@notes_bp.route('/notes')
@login_required
def view_notes():
    user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).all()
    print(f"Fetched {len(user_notes)} notes.")  # Debug print (remove after confirming functionality)
    return render_template('notes.html', notes=user_notes)
