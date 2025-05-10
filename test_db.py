from app import create_app
from app.models import db
from app.models.file import File

# Create the app instance
app = create_app()

# Enter the app context
with app.app_context():
    # Query the file table
    files = File.query.all()
    if files:
        for file in files:
            print(file.filename, file.tags)
    else:
        print("No files found in the database.")
