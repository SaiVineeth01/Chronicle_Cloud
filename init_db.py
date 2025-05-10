# init_db.py
from app import create_app
from app.database.database import init_db  # Correct import path

app = create_app()

# Initialize the database tables if they don't exist
with app.app_context():
    init_db()

print("Database tables created successfully!")
