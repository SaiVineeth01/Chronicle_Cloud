import eventlet
eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO
from app import create_app, db  # Import the create_app factory and db
from dotenv import load_dotenv
import os
from app import socketio

# Load environment variables from a .env file
load_dotenv()

# Create Flask app using the factory pattern
app = create_app()
socketio = SocketIO(app, async_mode='eventlet')

# Create all database tables (this should be done inside an app context)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
