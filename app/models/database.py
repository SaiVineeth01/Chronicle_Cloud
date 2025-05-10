from app import db

# Function to create the database tables
def init_db():
    db.create_all()
