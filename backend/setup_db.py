# -----------------------------
# setup_db.py
# -----------------------------
# This script will:
# 1. Connect to PostgreSQL
# 2. Create the database if it doesn't exist
# 3. Create tables based on models.py
# 4. Insert sample data from sample_data.sql if not already inserted

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
from app import app
from database import db
import models

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
# Step 5: Insert sample data
# -----------------------------
sample_sql_file = "database/sample_data.sql"

with app.app_context():
    with engine.begin() as connection:
        with open(sample_sql_file, "r") as f:
            sql_commands = f.read()

        statements = [
            stmt.strip() for stmt in sql_commands.split(";")
            if stmt.strip() and not stmt.strip().startswith("--")
        ]

        for stmt in statements:
            connection.execute(text(stmt))

print("Database setup complete!")
