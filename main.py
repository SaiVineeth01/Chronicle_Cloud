from app import create_app, db  # Import the create_app factory and db
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Create Flask app using the factory pattern
app = create_app()

# Create all database tables (this should be done inside an app context)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5001)

