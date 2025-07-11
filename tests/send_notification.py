# tests/send_notification.py

import sys
import os
from datetime import datetime

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, socketio, db
from app.models.notification import Notification

# Create and configure the Flask app
app = create_app()
app.app_context().push()

# Supported types
VALID_NOTIFICATION_TYPES = ['info', 'success', 'warning', 'error']

def send_notification_to_user(user_id, message, notif_type='info'):
    if notif_type not in VALID_NOTIFICATION_TYPES:
        print(f"⚠️ Invalid notification type '{notif_type}', defaulting to 'info'.")
        notif_type = 'info'

    created_at = datetime.now()

    notif = Notification(
        user_id=user_id,
        message=message,
        type=notif_type,
        created_at=created_at,
        read=False
    )

    db.session.add(notif)
    db.session.commit()

    socketio.emit('new_notification', {
        'id': notif.id,
        'user_id': notif.user_id,
        'message': notif.message,
        'type': notif.type,
        'created_at': notif.created_at.isoformat(),
        'read': notif.read
    }, to=None)

    print(f"✅ Notification sent to user {user_id} with type '{notif_type}'.")

# Example usage
if __name__ == '__main__':
    send_notification_to_user(
        1,
        "📬 Hi Pavan!!! You have seminar on monday! Be ready.",
        "info"
    )
    send_notification_to_user(
        1,
        "🚀 Successfully uploaded the blog",
        "success"
    )
    send_notification_to_user(
        1,
        "🚨 Hey Pavan! Please follow the rules and regulations of our community. Thank you!",
        "warning"
    )

