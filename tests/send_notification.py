import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.controllers.notifications_controller import create_notification
from app.models.user import User

app = create_app()

with app.app_context():
    user_id = 1
    user = User.query.get(user_id)
    if user:
        notif = create_notification(user.id, "hello honey welcome to our world!", notif_type="info")
        print("Notification created and sent:", notif)
    else:
        print(f"User with ID {user_id} does not exist.")
