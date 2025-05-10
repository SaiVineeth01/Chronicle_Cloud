from app.models import User
from app import db
from app.models.settings import Settings


# Get all users
def get_users():
    return User.query.all()

# Delete a user by ID
def delete_user(user_id):
    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
def get_settings():
    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        db.session.add(settings)
        db.session.commit()
    return settings

def update_settings(form_data):
    settings = Settings.query.first()  # assuming your Settings model exists
    settings.site_name = form_data.get('site_name')
    settings.theme = form_data.get('theme')
    settings.signup_enabled = form_data.get('signup_enabled') == 'true'
    settings.maintenance_mode = form_data.get('maintenance_mode') == 'true'
    settings.default_role = form_data.get('default_role')
    settings.email_notifications = form_data.get('email_notifications') == 'true'

    db.session.commit()  # Save changes to the database
