# clear_alembic.py
from sqlalchemy import text
from app import create_app, db

app = create_app()
with app.app_context():
    # Delete the old version entry
    db.session.execute(text("DELETE FROM alembic_version;"))
    db.session.commit()
    print("✅ alembic_version row deleted")
