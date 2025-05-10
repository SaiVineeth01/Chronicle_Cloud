from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

def create_admin():
    with app.app_context():  # Ensure app context is active
        # Create tables if they don't exist
        db.create_all()

        # Check if the admin user already exists by email
        existing_admin = User.query.filter_by(email='admin1@example.com').first()
        if existing_admin:
            print('Admin user already exists.')
            # If admin exists, update the password
            hashed_password = generate_password_hash('newadminpassword', method='scrypt')
            existing_admin.password_hash = hashed_password
            db.session.commit()
            print('Admin password updated successfully.')
            return

        # If admin does not exist, create a new admin user
        hashed_password = generate_password_hash('adminpassword', method='scrypt')

        # Create new admin user
        admin_user = User(
            username='admin1',
            email='admin1@example.com',
            password_hash=hashed_password,
            role='admin'  # Ensure this matches the role in your User model
        )

        # Add new admin to the database
        db.session.add(admin_user)
        db.session.commit()
        print('Admin user created successfully.')

if __name__ == '__main__':
    create_admin()
