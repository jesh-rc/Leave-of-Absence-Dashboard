# Leave-of-Absence-Dashboard

To set up the code and database, do the following:

cd backend
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python setup_db.py

## External Email Notification Integration

For Phase 3 we integrated the Mailgun email API to send notifications when leave requests are created and when their status changes.

### Overview

The backend calls the Mailgun REST API from `backend/services/email_service.py` using the `requests` library.  
Emails are sent in two cases

1. When an employee creates a leave request  
2. When a manager or admin updates the status of a leave request

We mapped a few sample employees from the database to real group member email addresses so the notifications can be tested in a real inbox.

### Configuration

Create a file `backend/.env` with at least the following variables

```env
DATABASE_URL=postgresql://postgres:YOURPASSWORD@localhost:5432/loa_db
SECRET_KEY=some_random_string

EMAIL_API_URL=https://api.mailgun.net/v3/YOUR_SANDBOX_DOMAIN/messages
EMAIL_API_KEY=your_mailgun_private_api_key
EMAIL_FROM_NAME=Leave Dashboard
EMAIL_FROM_ADDRESS=postmaster@YOUR_SANDBOX_DOMAIN
