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
2. Start the backend server using:
   flask run

3. Open Postman (or any API client).

4. Create a new request with the following details:

   Method: POST
   URL: http://127.0.0.1:5000/api/email/test
   Headers:
   - Content-Type: application/json

   Body (Raw JSON):
   {
     "subject": "Test Email",
     "body": "If you received this, the email notification feature is working."
   }

5. Send the request.

6. Check the inbox of the email addresses configured in `email_service.py` or in your `.env` file.
   For marking, the TA may replace these emails with their own.

If the email is received, the email notification feature is working correctly.

---

## Database Views Feature

The project includes several SQL views that are automatically created from `sql/views.sql` when the database setup script is run. Each view is exposed through a dedicated API endpoint.

### How to Use the Database Views

1. Initialize or refresh the database (this also creates all views):
   python setup_db.py

2. Start the backend server:
   flask run

3. Open a new terminal window.

4. Use curl to test each view endpoint. Examples:
   curl http://127.0.0.1:5000/api/views/view1
   curl http://127.0.0.1:5000/api/views/view2
   curl http://127.0.0.1:5000/api/views/view3

5. Each command will output JSON representing the rows returned by that SQL view.
   If JSON appears in the terminal, the view is functioning correctly.

---

## Summary for TA Testing

1. Run:
   python setup_db.py
   to initialize the database and create all views.

2. Run:
   flask run
   to start the backend server.

3. Test the SQL views using the provided curl commands.

4. Test the email feature by sending a POST request in Postman to the email endpoint.

If JSON is returned for each view and the test email is received, both features are working correctly.