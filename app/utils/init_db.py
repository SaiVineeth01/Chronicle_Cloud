from app import create_app
from app.database import init_db

app = create_app()

# Initialize the database tables using the function from app.database
with app.app_context():
    init_db()

print("Database tables created successfully!")
