import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

# Create app context
app = create_app()

with app.app_context():
    # Create admin user
    admin_user = User(
        username="admin",
        email="admin@example.com",
        role="admin"
    )

    # Set password using the set_password method
    admin_user.set_password("adminpassword")

    # Add the user to the session and commit to the database
    db.session.add(admin_user)
    db.session.commit()

    print("Admin user created successfully!")
