# app/routes/subscription_routes.py

from flask import Blueprint, request, jsonify
from app import db, socketio
from app.models import Subscriber, User, Notification
from datetime import datetime
from flask_login import login_required, current_user

subscription_bp = Blueprint('subscription', __name__, url_prefix='/subscription')


@subscription_bp.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    name = request.json.get('name')

    if not email:
        return jsonify({'status': 'error', 'message': 'Email is required'}), 400

    if Subscriber.query.filter_by(email=email).first():
        return jsonify({'status': 'exists', 'message': 'Already subscribed.'}), 200

    # Save new subscriber
    new_subscriber = Subscriber(email=email, subscribed_at=datetime.utcnow())
    db.session.add(new_subscriber)
    db.session.commit()

    # Create a system notification
    notif = Notification(
        user_id=None,
        message=f"New subscriber: {email}",
        type="success"
    )
    db.session.add(notif)
    db.session.commit()

    # Emit real-time notification via Socket.IO
    socketio.emit('new_notification', {
        "id": notif.id,
        "message": notif.message,
        "type": notif.type,
        "read": False,
        "created_at": notif.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }, broadcast=True)

    # Simulated email confirmation
    print(f"[LOG] Subscribed: {email} — Confirmation sent (simulated)")

    return jsonify({'status': 'success', 'message': 'Subscription confirmed!'}), 200


@subscription_bp.route('/broadcast', methods=['POST'])
def broadcast():
    data = request.json
    message = data.get('message')
    target = data.get('target')  # 'all' or 'subscribers'

    if not message or target not in ['all', 'subscribers']:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    if target == 'all':
        recipients = [u.email for u in User.query.all()]
    else:
        recipients = [s.email for s in Subscriber.query.all()]

    # Simulate message sending
    print(f"[BROADCAST] To {target.upper()} ({len(recipients)}): {message}")

    return jsonify({'status': 'success', 'message': f'Message broadcasted to {len(recipients)} users.'}), 200

@subscription_bp.route('/list')
@login_required
def subscriber_list():
    if current_user.role != 'admin':
        return "Access Denied", 403

    subscribers = Subscriber.query.all()
    return render_template('admin/subscribers.html', subscribers=subscribers)

