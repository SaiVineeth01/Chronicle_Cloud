import sys
import os
import time
from datetime import datetime
import pytz
from sqlalchemy.exc import OperationalError

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, socketio, db
from app.models.notification import Notification

# Supported notification types
VALID_NOTIFICATION_TYPES = ['info', 'success', 'warning', 'error']

# Create Flask app
app = create_app()

def send_notification_to_user(user_id, message, notif_type='info'):
    if notif_type not in VALID_NOTIFICATION_TYPES:
        print(f"⚠️ Invalid notification type '{notif_type}', defaulting to 'info'.")
        notif_type = 'info'

    # Current UTC time
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)

    notif = Notification(
        user_id=user_id,
        message=message,
        type=notif_type,
        created_at=utc_now,
        read=False
    )

    db.session.add(notif)

    # Try DB commit with retry for Neon cold starts
    for attempt in range(3):
        try:
            db.session.commit()
            break
        except OperationalError as e:
            print(f"🔁 Retrying DB commit ({attempt+1}/3)...")
            time.sleep(5)
    else:
        print("❌ Failed to commit notification after 3 attempts.")
        return

    # Convert UTC to IST for UI
    ist_time = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))

    # Emit via SocketIO
    socketio.emit('new_notification', {
        'id': notif.id,
        'user_id': notif.user_id,
        'message': notif.message,
        'type': notif.type,
        'created_at': ist_time.strftime('%d-%m-%Y %I:%M %p'),
        'read': notif.read
    }, to=None)

    print(f"✅ Notification sent to user {user_id} ({notif_type}) at {ist_time.strftime('%d-%m-%Y %I:%M %p')} IST.")

if __name__ == '__main__':
    with app.app_context():
        # Optional: Wake Neon if needed
        try:
            with db.engine.connect() as conn:
                conn.execute("SELECT 1")
                print("✅ Neon DB connection successful.")
        except Exception as e:
            print("❌ Failed to connect to Neon DB:", e)
            sys.exit(1)

        # Send test notifications
        send_notification_to_user(
            1, "📬 Hi Honey!!! You have seminar on Monday! Be ready.", "info"
        )
        send_notification_to_user(
            1, "🚀 Successfully uploaded the blog", "success"
        )
        send_notification_to_user(
            1, "🚨 Hey Honey! Please follow the rules and regulations of our community. Thank you!", "warning"
        )
