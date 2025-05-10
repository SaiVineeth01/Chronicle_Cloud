import os
from app import db
from app.models import File
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'app/static/uploads'

# Function to upload a file
def upload_file(user_id, file):
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    
    uploaded_file = File(user_id=user_id, filename=filename)
    db.session.add(uploaded_file)
    db.session.commit()

# Function to get all uploaded files of a user
def get_user_files(user_id):
    return File.query.filter_by(user_id=user_id).all()
