import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User

app = create_app()

admins_to_create = [
    {"username": "admin3", "email": "admin3@example.com", "password": "admin3password"},
    {"username": "admin4", "email": "admin4@example.com", "password": "admin4password"},
    {"username": "ram(admin)", "email": "ram6@example.com", "password": "ram5password"},
]

with app.app_context():
    for admin in admins_to_create:
        existing_user = User.query.filter_by(username=admin["username"]).first()
        if existing_user:
            print(f"Admin user {admin['username']} already exists.")
        else:
            new_admin = User(
                username=admin["username"],
                email=admin["email"],
                role="admin"
            )
            new_admin.set_password(admin["password"])
            db.session.add(new_admin)
            print(f"Admin user {admin['username']} created.")
    db.session.commit()
    print("All admin users processed.")
