# app/sockets/events.py

from app import socketio
from flask_socketio import emit
from flask_login import current_user
from flask_socketio import join_room

# ✅ WebSocket event handler for testing or future use
@socketio.on('join')
def handle_join(data):
    user_id = data.get('user_id')
    if user_id:
        join_room(str(user_id))
        print(f"User {user_id} joined room {user_id}")



@socketio.on('my_custom_event')
def handle_custom_event(json_data):
    print('✅ Received custom event:', json_data)
    emit('response', {'message': '✅ Server received your message!'})

# ✅ Function to send a notification to a specific user (via WebSocket)
def send_notification_to_user(user_id, notification_data):
    """
    Sends a real-time notification to a specific user via WebSocket.

    Args:
        user_id (int): The ID of the user to send the notification to.
        notification_data (dict): The notification payload.
    """
    print(f"✅ Sending notification to user {user_id}: {notification_data}")
    socketio.emit('new_notification', notification_data, room=user_id)


