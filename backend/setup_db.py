# -----------------------------
# setup_db.py
# -----------------------------
# This script will:
# 1. Connect to PostgreSQL
# 2. Create the database if it doesn't exist
# 3. Create tables based on models.py
# 4. Insert sample data from sample_data.sql if not already inserted

# Run this code in the backend/ directory

import os                               # To access environment variables
from sqlalchemy import create_engine, text    # To create a SQLAlchemy engine to connect to the database
from sqlalchemy_utils import database_exists, create_database # To check if DB exists and create it if not
from dotenv import load_dotenv          # To load environment variables from .env file
from app import app, db                 # Import the Flask app and SQLAlchemy db object
import models                           # Import models for table definitions

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()  # Reads .env file

DATABASE_URL = os.getenv("DATABASE_URL")  # e.g., "postgresql://postgres:password@localhost:5432/loa_db"

if DATABASE_URL is None:                  # If the URL is missing throw an exception
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
# Step 2: Connect to the database
# -----------------------------
engine = create_engine(DATABASE_URL)  # SQLAlchemy engine

# -----------------------------
# Step 3: Create tables if they don't exist
# -----------------------------
print("Creating tables (if not exist)...")
with app.app_context():  # <-- ensures Flask knows the app context
    db.create_all()      # Reads models.py and creates tables

# -----------------------------
# Step 4: Insert sample data
# -----------------------------
sample_sql_file = "database/sample_data.sql" # Path to sample data SQL file

with app.app_context():
    with engine.begin() as connection:  # <-- begin() auto-commits
        with open(sample_sql_file, "r") as f:
            sql_commands = f.read()

        # Remove comments and split by semicolon
        statements = [
            stmt.strip() for stmt in sql_commands.split(";")
            if stmt.strip() and not stmt.strip().startswith("--")
        ]

        for stmt in statements:
            connection.execute(text(stmt))




print("Database setup complete!")
