import eventlet
eventlet.monkey_patch()

from app import create_app, db, socketio
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ Ensure /tmp/ DB path is initialized for Render
if os.environ.get("RENDER"):
    os.makedirs("/tmp", exist_ok=True)
    open("/tmp/chroniclecloud.db", 'a').close()

app = create_app()

# ✅ Create DB tables (only once in app context)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("✅ Flask app created")
    print("🚀 Starting server on http://localhost:5000")
    socketio.run(app, debug=True, use_reloader=True, host='0.0.0.0', port=5000)