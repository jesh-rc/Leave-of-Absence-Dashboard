import os                       # Used to access environment variables
from dotenv import load_dotenv  # Used to load environment variables from a .env file

load_dotenv()  # load variables from .env

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") # Read the connection string from the .env file
SQLALCHEMY_TRACK_MODIFICATIONS = False # Disable tracking modifications to save resources

# secret key for sessions
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")