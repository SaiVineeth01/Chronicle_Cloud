import eventlet
eventlet.monkey_patch()  # Must be at the top before importing anything else

from app import create_app, db, socketio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = create_app()

# Create tables if not present (safe in app context)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("✅ Flask app created")
    print("🚀 Starting SocketIO server at http://localhost:5000")

    # Start server using Eventlet worker
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
