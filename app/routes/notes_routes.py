from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app.models import Note, Settings
from app import db
from flask_login import login_required, current_user
from app.utils.activity_logger import log_activity
from bs4 import BeautifulSoup  # ✅ For cleaning HTML

# Notes Blueprint
notes_bp = Blueprint('notes', __name__)

# ✅ View all approved notes
@notes_bp.route('/view_notes')
@login_required
def view_notes():
    if current_user.role == 'admin':
        notes = Note.query.order_by(Note.created_at.desc()).all()
    else:
        notes = Note.query.filter_by(approved=True).order_by(Note.created_at.desc()).all()

    notes = sorted(notes, key=lambda note: 0 if note.user.role == 'admin' else 1)
    return render_template('notes.html', notes=notes)

# ✅ Create a new note
@notes_bp.route('/notes/create', methods=['POST'])
@login_required
def create_note():
    title = request.form['title']
    category = request.form.get('category')
    due_date = request.form.get('due_date')
    raw_content = request.form['content']

    # Clean HTML tags
    soup = BeautifulSoup(raw_content, 'html.parser')
    plain_content = soup.get_text(separator=' ', strip=True)

    if not title:
        flash("Title is required!", "danger")
        return redirect(url_for('notes.view_notes'))

    settings = Settings.query.first()
    moderation_enabled = settings.moderation_required if settings else True

    note = Note(
        title=title,
        category=category,
        due_date=due_date,
        content=plain_content,
        user_id=current_user.id,
        approved=(not moderation_enabled) or current_user.role == 'admin'
    )
    db.session.add(note)
    db.session.commit()
    log_activity(current_user.id, "Note", f'Created note: "{note.title}"')

    if note.approved:
        flash("Note created successfully!", "success")
    else:
        flash("Note submitted for moderation.", "info")

    return redirect(url_for('notes.view_notes'))

# ✅ Delete a specific note
@notes_bp.route('/notes/delete/<int:note_id>', methods=['POST', 'DELETE'])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)

    if not note:
        if request.method == 'DELETE':
            return jsonify({'success': False, 'error': 'Note not found'}), 404
        flash("Note not found.", "danger")
        return redirect(url_for('notes.view_notes'))

    if current_user.id != note.user_id and current_user.role != 'admin':
        if request.method == 'DELETE':
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        flash("You do not have permission to delete this note.", "danger")
        return redirect(url_for('notes.view_notes'))

    log_activity(current_user.id, "Note", f'Deleted note: "{note.title}"')

    db.session.delete(note)
    db.session.commit()

    if request.method == 'DELETE':
        return jsonify({'success': True}), 200

    flash("Note deleted successfully.", "success")
    return redirect(url_for('notes.view_notes'))

# ✅ Delete all notes
@notes_bp.route('/notes/delete_all', methods=['POST', 'DELETE'])
@login_required
def delete_all_notes():
    if current_user.role != 'admin':
        if request.method == 'DELETE':
            return jsonify({'success': False, 'error': 'Only admins can delete all notes.'}), 403
        flash("Only admins can delete all notes.", "danger")
        return redirect(url_for('notes.view_notes'))

    log_activity(current_user.id, "Note", f'Deleted all notes')

    Note.query.delete()
    db.session.commit()

    if request.method == 'DELETE':
        return jsonify({'success': True}), 200

    flash("All notes deleted successfully.", "success")
    return redirect(url_for('notes.view_notes'))

# ✅ User dashboard
@notes_bp.route('/dashboard')
@login_required
def dashboard():
    user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).all()
    return render_template('dashboard.html', notes=user_notes)

# ✅ Edit note
@notes_bp.route('/notes/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get(note_id)

    if not note:
        flash("Note not found!", "danger")
        return redirect(url_for('notes.view_notes'))

    if current_user.id != note.user_id and current_user.role != 'admin':
        flash("You are not authorized to edit this note.", "danger")
        return redirect(url_for('notes.view_notes'))

    if request.method == 'POST':
        note.title = request.form['title']
        note.category = request.form.get('category')
        note.due_date = request.form.get('due_date')

        raw_content = request.form['content']
        soup = BeautifulSoup(raw_content, 'html.parser')
        note.content = soup.get_text(separator=' ', strip=True)

        db.session.commit()
        flash("Note updated successfully!", "success")
        return redirect(url_for('notes.view_notes'))

    return render_template('edit_note.html', note=note)

# ✅ Moderate pending notes
@notes_bp.route('/notes/moderate')
@login_required
def moderate_notes():
    if current_user.role != 'admin':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('notes.view_notes'))

    notes = Note.query.filter_by(approved=False).order_by(Note.created_at.desc()).all()
    return render_template('moderate_notes.html', notes=notes)

# ✅ Approve note
@notes_bp.route('/notes/approve/<int:note_id>', methods=['POST'])
@login_required
def approve_note(note_id):
    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('notes.view_notes'))

    note = Note.query.get_or_404(note_id)
    note.approved = True
    db.session.commit()
    flash("Note approved successfully.", "success")
    return redirect(url_for('notes.moderate_notes'))

# ✅ Reject note
@notes_bp.route('/notes/reject/<int:note_id>', methods=['POST'])
@login_required
def reject_note(note_id):
    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('notes.view_notes'))

    note = Note.query.get_or_404(note_id)
    log_activity(current_user.id, "Note", f'Rejected note: "{note.title}" (deleted)')
    db.session.delete(note)
    db.session.commit()
    flash("Note rejected and deleted.", "warning")
    return redirect(url_for('notes.moderate_notes'))
