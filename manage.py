import os
from dotenv import load_dotenv

# ✅ Load the .env file BEFORE anything else
load_dotenv()

from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
