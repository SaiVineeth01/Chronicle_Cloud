# add_test_notification.py
from app import db
from app.models.notification import Notification
from app.models.user import User

# Get an existing user or create one (ensure the user exists in the database)
user = User.query.first()  # You can adjust this to get a specific user or create one if needed.

if user:
    new_notif = Notification(message="Test Notification", type="info", user_id=user.id)
    db.session.add(new_notif)
    db.session.commit()
    print("Test notification added successfully!")
else:
    print("No user found. Please create a user first.")
