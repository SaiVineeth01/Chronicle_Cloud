import os
import platform

if platform.system() != 'Windows':
    import eventlet
    eventlet.monkey_patch()  # Only patch on Linux (Render)

from app import create_app, db, socketio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = create_app()

# Create tables if not present
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("✅ Flask app created")
    print("🚀 Starting server...")

    # On Windows (local dev), use default Flask dev server
    if platform.system() == 'Windows':
        socketio.run(app, host='127.0.0.1', port=5000, debug=True)
    else:
        # On Render/Linux, use Eventlet
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
