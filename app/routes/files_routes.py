from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import pytz
from flask_login import login_required, current_user
from app import db
from app.models.file import File
from app.utils.activity_logger import log_activity

files_bp = Blueprint('files', __name__)
UPLOAD_FOLDER = 'app/static/uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'txt', 'csv', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@files_bp.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(save_path)

            file = File(
                filename=filename,
                user_id=current_user.id,
                upload_time=datetime.utcnow()
            )
            db.session.add(file)
            db.session.commit()

            log_activity(current_user.id, f"Uploaded file: {filename}")
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('files.list_files'))
        else:
            flash('Invalid file format!', 'danger')
    return render_template('upload_file.html')

@files_bp.route('/files')
@login_required
def list_files():
    files = File.query.order_by(File.upload_time.desc()).all()
    for file in files:
        file.upload_time_local = file.upload_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Kolkata"))
    return render_template('files.html', files=files)

@files_bp.route('/download_file/<filename>')
@login_required
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        log_activity(current_user.id, f"Downloaded file: {filename}")
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    else:
        flash("File not found on the server.", "danger")
        return redirect(url_for('files.list_files'))

@files_bp.route('/delete_file/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    if current_user.id != file.user_id and not current_user.is_admin:
        flash("Unauthorized to delete this file.", "danger")
        return redirect(url_for('files.list_files'))

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(file)
    db.session.commit()
    log_activity(current_user.id, f"Deleted file: {file.filename}")
    flash("File deleted successfully!", "success")
    return redirect(url_for('files.list_files'))
