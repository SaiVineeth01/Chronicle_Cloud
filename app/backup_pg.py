import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection URI format:
# postgresql://<user>:<password>@<host>:<port>/<database>
db_uri = "postgresql://chronicle_user:2xZJzWYoq7qfXTJV1pVg4bDyziesAd9t@dpg-d0fnqqadbo4c73als7g0-a.frankfurt-postgres.render.com/chronicle_db"  # Add your database URI here

# Create engine
engine = create_engine(db_uri)

# Table to backup (we'll only backup the 'notifications' table now)
tables = ['notifications']  # Only the notifications table

# Backup each table to CSV
for table in tables:
    try:
        # Read data from the notifications table
        df = pd.read_sql(f"SELECT * FROM {table}", engine)
        
        # Save the data to a CSV file
        df.to_csv(f"{table}_backup.csv", index=False)
        
        print(f"✅ {table} backed up to {table}_backup.csv")
    except Exception as e:
        print(f"❌ Failed to back up {table}: {e}")
