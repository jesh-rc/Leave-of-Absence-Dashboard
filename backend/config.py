import os                       # Used to access environment variables
from dotenv import load_dotenv  # Used to load environment variables from a .env file

load_dotenv()  # load variables from .env

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") # Read the connection string from the .env file
SQLALCHEMY_TRACK_MODIFICATIONS = False # Disable tracking modifications to save resources

# secret key for sessions
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

# email service configuration
EMAIL_API_URL = os.getenv("EMAIL_API_URL")          # example: https://api.mailgun.net/v3/YOUR_DOMAIN/messages
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")          # your Mailgun private API key
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "Leave Dashboard")
EMAIL_FROM_ADDRESS = os.getenv("EMAIL_FROM_ADDRESS", "no-reply@example.com")