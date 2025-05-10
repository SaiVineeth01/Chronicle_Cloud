import os
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from app.models.file import db, File

# Blueprint setup
files_bp = Blueprint('files_bp', __name__, template_folder='../templates')

# Constants
UPLOAD_FOLDER = 'C:\\Users\\hh\\Chronicle_Cloud\\app\\static\\uploads'  # Correct path
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'txt'}

# Helper: check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route: File list page
@files_bp.route('/files')
def list_files():
    files = File.query.all()
    return render_template('files.html', files=files)

# Route: Handle file upload
@files_bp.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part in the request', 'danger')
        return redirect(url_for('files_bp.list_files'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected', 'warning')
        return redirect(url_for('files_bp.list_files'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Ensure upload folder exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(filepath)

        # Save file metadata in the database
        new_file = File(filename=filename, filepath=os.path.join('uploads', filename), tags='')  # Save relative path
        db.session.add(new_file)
        db.session.commit()

        flash(f'File "{filename}" uploaded successfully!', 'success')
        return redirect(url_for('files_bp.list_files'))

    flash('Invalid file type. Only PDF, JPG, JPEG, PNG, and TXT are allowed.', 'danger')
    return redirect(url_for('files_bp.list_files'))

# Route: Download file
@files_bp.route('/download-file/<int:file_id>')
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    if not os.path.exists(os.path.join(UPLOAD_FOLDER, file.filename)):  # Use full path to check existence
        flash('File not found.', 'danger')
        return redirect(url_for('files_bp.list_files'))
    print(f"Attempting to send file from: {file.filepath}")
    return send_file(os.path.join(UPLOAD_FOLDER, file.filename), as_attachment=True)

# Route: Delete file
@files_bp.route('/delete-file/<int:file_id>', methods=['POST'])
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    try:
        # Delete the file from the filesystem
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        # Delete the record from DB
        db.session.delete(file)
        db.session.commit()
        flash(f'File "{file.filename}" deleted.', 'success')
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'danger')
    return redirect(url_for('files_bp.list_files'))
