# app/controllers/notifications_controller.py

from app.models.notification import Notification

def get_notifications(user_id):
    from app import db
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    return [n.to_dict() for n in notifications]

def mark_notification_as_read(notification_id, user_id):
    from app import db
    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    if notification:
        notification.read = True
        db.session.commit()
        return {'status': 'success', 'message': 'Notification marked as read'}
    return {'status': 'error', 'message': 'Notification not found'}

def delete_all_notifications(user_id):
    from app import db
    Notification.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return {'status': 'success', 'message': 'All notifications deleted'}

def create_notification(user_id, message, notif_type='info'):
    from app import db, socketio
    new_notification = Notification(
        user_id=user_id,
        message=message,
        type=notif_type
    )
    db.session.add(new_notification)
    db.session.commit()

    # Prepare notification data
    notification_data = {
        'id': new_notification.id,
        'message': new_notification.message,
        'created_at': new_notification.created_at.strftime("%Y-%m-%d %H:%M"),
        'read': new_notification.read,
        'type': new_notification.type,
    }

    # Emit the notification in real-time to the user's room
    socketio.emit('new_notification', notification_data, room=str(user_id))

    return notification_data
