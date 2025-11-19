# Leave-of-Absence-Dashboard

To set up the code and database, do the following:

cd backend
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python setup_db.py

## External Email Notification Integration

The project includes an external email notification system that allows the backend to send emails using an external email API.

### How to Use the Email Feature

1. Make sure your `.env` file contains the required email configuration values used by `services/email_service.py`.
Create a file `backend/.env` with at least the following variables

```env
DATABASE_URL=postgresql://postgres:YOURPASSWORD@localhost:5432/loa_db
SECRET_KEY=some_random_string

EMAIL_API_URL=https://api.mailgun.net/v3/YOUR_SANDBOX_DOMAIN/messages
EMAIL_API_KEY=your_mailgun_private_api_key
EMAIL_FROM_NAME=Leave Dashboard
EMAIL_FROM_ADDRESS=postmaster@YOUR_SANDBOX_DOMAIN
