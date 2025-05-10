from flask import Blueprint, render_template, jsonify, request
from app.models import Notification

notifications_bp = Blueprint('notifications', __name__)

# Fetch notifications
@notifications_bp.route('/get_notifications')
def get_notifications():
    notifications = Notification.query.all()
    notifications_list = [
        {
            'id': notif.id,
            'message': notif.message,
            'created_at': notif.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'read': notif.read,
            'type': notif.type
        }
        for notif in notifications
    ]
    return jsonify(notifications_list)

# Mark a notification as read
@notifications_bp.route('/mark_read/<int:id>', methods=['POST'])
def mark_as_read(id):
    notif = Notification.query.get(id)
    if notif:
        notif.read = True
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 404

# Delete all notifications
@notifications_bp.route('/delete_all', methods=['POST'])
def delete_all():
    Notification.query.delete()
    db.session.commit()
    return jsonify({'status': 'success'})
