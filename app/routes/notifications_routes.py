# app/routes/notifications_routes.py

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.controllers.notifications_controller import (
    get_notifications,
    mark_notification_as_read,
    delete_all_notifications,
)

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/get_notifications', methods=['GET'])
@login_required
def get_all_notifications():
    return jsonify(get_notifications(current_user.id))

@notifications_bp.route('/mark_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_read(notification_id):
    result = mark_notification_as_read(notification_id, current_user.id)
    return jsonify(result)

@notifications_bp.route('/delete_all', methods=['POST'])
@login_required
def delete_all():
    result = delete_all_notifications(current_user.id)
    return jsonify(result)
