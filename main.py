import eventlet
eventlet.monkey_patch()

import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from app import create_app, db, socketio

# Load environment variables
load_dotenv()

# Create app
app = create_app()
migrate = Migrate(app, db)

# Create DB tables if not already there
with app.app_context():
    db.create_all()

# ✅ Run differently depending on environment
if __name__ == '__main__':
    if os.environ.get("RENDER", "").lower() == "true":
        print("🚀 Render production mode. Gunicorn will handle running the app.")
    else:
        print("✅ Local development mode")
        print("🚀 Starting SocketIO server at http://localhost:5000")
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
