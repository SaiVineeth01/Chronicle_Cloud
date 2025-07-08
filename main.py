import eventlet
eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO
from app import create_app, db
from dotenv import load_dotenv
import os
from app import socketio


load_dotenv()


app = create_app()
socketio = SocketIO(app, async_mode='eventlet')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app = create_app()

    # Optional: confirm app created
    print("✅ Flask app created")

    # Optional: show environment and port
    print("🚀 Starting server on http://localhost:5000")

    # Start socketio app
    try:
        socketio.run(app, debug=True, use_reloader=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
