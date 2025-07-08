from app.models.activity import Activity
from app.models.user import User  # ✅ Make sure to import User
from app import db

def log_activity(user_id, action_type, description):
    """Logs a user activity with ID, username, type, and description."""

    user = User.query.get(user_id)  # ✅ Fetch the user using ID
    if not user:
        return  # User not found, avoid logging

    activity = Activity(
        user_id=user.id,
        username=user.username,
        action_type=action_type,
        description=description
    )
    db.session.add(activity)
    db.session.commit()
