# tests/add_users.py

import sys
import os

# Add app root to the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User  # adjust if your user model path is different

app = create_app()

# List of regular users to create
users_to_create = [
    {"username": "user1", "email": "user1@example.com", "password": "user1password"},
    {"username": "user2", "email": "user2@example.com", "password": "user2password"},
    {"username": "vineeth", "email": "vineeth@example.com", "password": "vineeth123"},
]

with app.app_context():
    for user_data in users_to_create:
        existing_user = User.query.filter_by(username=user_data["username"]).first()
        if existing_user:
            print(f"User {user_data['username']} already exists.")
        else:
            new_user = User(
                username=user_data["username"],
                email=user_data["email"],
                role="user"  # Set role explicitly as "user"
            )
            new_user.set_password(user_data["password"])  # assumes set_password exists
            db.session.add(new_user)
            print(f"User {user_data['username']} created.")
    db.session.commit()
    print("✅ All users processed.")
