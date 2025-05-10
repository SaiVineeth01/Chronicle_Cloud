from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app.models import Note
from app import db
from flask_login import login_required, current_user

# Create a Blueprint instance for notes
notes_bp = Blueprint('notes', __name__)

# Fetch all notes
@notes_bp.route('/view_notes')  # Update the route name here
def view_notes():
    notes = Note.query.all()  # Fetch all notes from the database
    return render_template('notes.html', notes=notes)

# Create a new note (POST request)
@notes_bp.route('/notes/create', methods=['POST'])
def create_note():
    title = request.form['title']
    category = request.form.get('category')
    due_date = request.form.get('due_date')
    content = request.form['content']

    if not title:
        flash("Title is required!", "error")
        return redirect(url_for('notes.create_note'))  # Ensure this route matches the create note route

    # Create and save the new note
    note = Note(
        title=title,
        category=category,
        due_date=due_date,
        content=content,
        user_id=current_user.id  # Use the current logged-in user's ID
    )
    db.session.add(note)
    db.session.commit()  # Ensure the new note is saved to the database
    flash("Note created successfully!", "success")

    return redirect(url_for('notes.view_notes'))  # Redirect to the 'view_notes' route

# Delete a specific note
@notes_bp.route('/notes/delete/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'success': True})

# Delete all notes
@notes_bp.route('/notes/delete_all', methods=['DELETE'])
def delete_all_notes():
    Note.query.delete()
    db.session.commit()
    return jsonify({'success': True})

# Dashboard route (for logged-in users only)
@notes_bp.route('/dashboard')
@login_required
def dashboard():
    user_notes = Note.query.filter_by(user_id=current_user.id).all()  # Get notes for the logged-in user
    return render_template('dashboard.html', notes=user_notes)
@notes_bp.route('/notes/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if request.method == 'POST':
        # Update the note details
        note.title = request.form['title']
        note.category = request.form.get('category')
        note.due_date = request.form.get('due_date')
        note.content = request.form['content']

        db.session.commit()
        flash("Note updated successfully!", "success")
        return redirect(url_for('notes.view_notes'))  # Redirect to the view notes page

    # Render the edit note form
    return render_template('edit_note.html', note=note)


