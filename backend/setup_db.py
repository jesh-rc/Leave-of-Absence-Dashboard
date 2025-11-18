# -----------------------------
# setup_db.py
# -----------------------------
# This script will:
# 1. Connect to PostgreSQL
# 2. Create the database if it doesn't exist
# 3. Create tables based on models.py
# 4. Insert sample data from sample_data.sql
# 5. Create SQL views from views.sql
#
# Run this code in the backend/ directory

import os
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()  # Reads .env file
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise Exception("DATABASE_URL not found in .env")

# -----------------------------
# Step 1: Ensure database exists
# -----------------------------
if not database_exists(DATABASE_URL):
    print("Database does not exist. Creating database...")
    create_database(DATABASE_URL)
else:
    print("Database already exists.")

# -----------------------------
# Step 2: IMPORT app + db AFTER creating/checking the DB
# IMPORTANT: This order prevents circular imports!
# -----------------------------
from app import app          # your Flask app factory / instance
from database import db      # SQLAlchemy instance
import models                # ensures models are registered with SQLAlchemy

# -----------------------------
# Step 3: Connect engine
# -----------------------------
engine = create_engine(DATABASE_URL)

# -----------------------------
# Step 4: Create tables
# -----------------------------
print("Creating tables (if not exist)...")
with app.app_context():
    db.create_all()

# -----------------------------
# Step 5: Insert sample data (only if not already inserted)
# -----------------------------
sample_sql_file = "database/sample_data.sql"

with app.app_context():
    with engine.begin() as connection:
        # check if sample data is already there
        result = connection.execute(text("SELECT COUNT(*) FROM company"))
        company_count = result.scalar()

        if company_count and company_count > 0:
            print("Sample data already present, skipping sample_data.sql.")
        else:
            print("Inserting sample data from sample_data.sql...")
            with open(sample_sql_file, "r") as f:
                sql_commands = f.read()

            statements = [
                stmt.strip()
                for stmt in sql_commands.split(";")
                if stmt.strip() and not stmt.strip().startswith("--")
            ]

            for stmt in statements:
                connection.execute(text(stmt))

# -----------------------------
# Step 6: Create Views
# -----------------------------
views_sql_path = "database/views.sql"

with app.app_context():
    with open(views_sql_path, "r") as f:
        sql = f.read()

    view_statements = [
        stmt.strip()
        for stmt in sql.split(";")
        if stmt.strip() and not stmt.strip().startswith("--")
    ]

    for stmt in view_statements:
        db.session.execute(text(stmt))

    db.session.commit()
    print("SQL views created.")

print("Database setup complete!")
