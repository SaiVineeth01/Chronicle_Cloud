from app import db


class Settings(db.Model):
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default="ChronicleCloud")
    theme = db.Column(db.String(10), default='light')
    signup_enabled = db.Column(db.Boolean, default=True)
    maintenance_mode = db.Column(db.Boolean, default=False)
    default_role = db.Column(db.String(20), default='user')
    email_notifications = db.Column(db.Boolean, default=True)
    admin_email = db.Column(db.String(100), default="admin@chroniclecloud.com")
    moderation_required = db.Column(db.Boolean, default=True)

