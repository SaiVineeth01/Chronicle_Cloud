import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from app.models.file import db, File
from app.utils.activity_logger import log_activity
from app.models import User
from pytz import timezone
from datetime import datetime

files_bp = Blueprint('files_bp', __name__, template_folder='../templates')

# Dynamically determine the upload folder relative to the app root
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'static', 'uploads')

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'txt'}

# Utility: Check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 🗂️ Route: View Files
@files_bp.route('/files')
@login_required
def list_files():
    files = File.query.order_by(File.id.desc()).all()
    ist = timezone('Asia/Kolkata')

    for f in files:
        f.uploader = User.query.get(f.uploaded_by)
        if f.uploaded_at:
            f.uploaded_at_ist = f.uploaded_at.astimezone(ist)

    return render_template('files.html', files=files)

# ⬆️ Route: Upload File
@files_bp.route('/upload-file', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part in the request', 'danger')
        return redirect(url_for('files_bp.list_files'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected.', 'warning')
        return redirect(url_for('files_bp.list_files'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        full_path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(full_path)

        # Save metadata to database
        new_file = File(
            filename=filename,
            filepath=os.path.join('uploads', filename),  # Relative for static folder
            tags='',
            uploaded_by=current_user.id
        )
        db.session.add(new_file)
        db.session.commit()

        log_activity(current_user.id, "Uploaded File", f"File '{filename}' uploaded.")
        flash(f'File "{filename}" uploaded successfully.', 'success')
        return redirect(url_for('files_bp.list_files'))

    flash('Invalid file type. Allowed: PDF, JPG, JPEG, PNG, TXT.', 'danger')
    return redirect(url_for('files_bp.list_files'))

# ⬇️ Route: Download File
@files_bp.route('/download-file/<int:file_id>')
@login_required
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    full_path = os.path.join(UPLOAD_FOLDER, file.filename)

    if not os.path.exists(full_path):
        flash('File not found on the server. Please contact admin.', 'danger')
        return redirect(url_for('files_bp.list_files'))

    log_activity(current_user.id, "Downloaded File", f'File "{file.filename}" downloaded.')
    return send_file(full_path, as_attachment=True)

# ❌ Route: Delete File
@files_bp.route('/delete-file/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    uploader = User.query.get(file.uploaded_by)

    # Permissions
    if current_user.role != 'admin':
        if file.uploaded_by != current_user.id:
            flash('Access denied: Only admins or owners can delete this file.', 'danger')
            return redirect(url_for('files_bp.list_files'))

        if uploader and uploader.role == 'admin':
            flash('Access denied: You cannot delete files uploaded by admins.', 'danger')
            return redirect(url_for('files_bp.list_files'))

    try:
        full_path = os.path.join(UPLOAD_FOLDER, file.filename)
        if os.path.exists(full_path):
            os.remove(full_path)

        db.session.delete(file)
        db.session.commit()

        log_activity(current_user.id, "Deleted File", f'File "{file.filename}" deleted.')
        flash(f'File "{file.filename}" deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting file: {str(e)}', 'danger')

    return redirect(url_for('files_bp.list_files'))
