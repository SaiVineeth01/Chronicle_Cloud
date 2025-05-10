import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.models.file import db, File

# Blueprint setup
files_bp = Blueprint('files_bp', __name__)

# Constants for file upload
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'txt'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to handle file upload
@files_bp.route('/upload-file', methods=['POST'])
def upload_file():
    # Check if file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # Check if file has a filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Check if file type is allowed
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Save the file to the specified path
        file.save(filepath)

        # Save file metadata to the database
        new_file = File(filename=filename, filepath=filepath, tags='')  # Assuming 'tags' is optional
        db.session.add(new_file)
        db.session.commit()

        # Return success message with file details
        return jsonify({
            "message": "File uploaded successfully",
            "file": {
                "filename": filename,
                "filepath": filepath
            }
        })

    return jsonify({"error": "Invalid file type. Only PDF, JPG, JPEG, PNG, and TXT are allowed."}), 400

# Route to retrieve all files
@files_bp.route('/get-files', methods=['GET'])
def get_files():
    files = File.query.all()
    return jsonify([{
        "id": file.id,
        "filename": file.filename,
        "tags": file.tags,
        "filepath": file.filepath
    } for file in files])

# Route to add tags to a file by its ID
@files_bp.route('/add-tags/<int:file_id>', methods=['POST'])
def add_tags(file_id):
    # Retrieve the file by ID
    file = File.query.get(file_id)
    if not file:
        return jsonify({"error": "File not found"}), 404

    # Retrieve tags from the request
    tags = request.form.get('tags')
    if tags:
        file.tags = tags
        db.session.commit()
        return jsonify({
            "message": "Tags added successfully",
            "tags": file.tags
        })

    return jsonify({"error": "No tags provided"}), 400
