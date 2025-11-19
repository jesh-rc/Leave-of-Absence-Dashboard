import requests

from config import (
    EMAIL_API_URL,
    EMAIL_API_KEY,
    EMAIL_FROM_NAME,
    EMAIL_FROM_ADDRESS,
)
from models import Employee, UserAccount  # 🔹 add UserAccount import


# Optional: keep a mapping for old hard-coded demo accounts
# This is now used as a *fallback* if username is not an email.
EMPLOYEE_EMAILS = {
    (1, 101): "vishnu.piraliyil@ontariotechu.net",
    (1, 102): "risanth.sivarajah@ontariotechu.net",
    (1, 103): "wahab.alam@ontariotechu.net",
    (1, 104): "jeshurun.constantine@ontariotechu.net",
    # add more if needed
}


def get_employee_email(cid, eid):
    """
    Determine which email to use for this employee.

    Priority:
      1. user_account.username, if it looks like a real email (used for
         employees created via the Admin 'Create Employee' form).
      2. Fallback to EMPLOYEE_EMAILS mapping for older hard-coded demo users.
    """
    # 1) Try to read from user_account.username
    ua = UserAccount.query.filter_by(cid=cid, eid=eid).first()
    if ua and ua.username:
        username = ua.username.strip()
        if "@" in username:
            # Treat username as an email address
            return username

    # 2) Fallback: old hard-coded mapping
    return EMPLOYEE_EMAILS.get((cid, eid))


def send_raw_email(to_email, subject, text_body):
    """
    Low level helper that calls the external Mailgun API.
    """
    if not EMAIL_API_URL or not EMAIL_API_KEY:
        print("Email API not configured, skipping send")
        print(f"  To: {to_email}")
        print(f"  Subject: {subject}")
        print(f"  Body:\n{text_body}")
        return False

    print(f"Sending email to {to_email} with subject {subject}")

    response = requests.post(
        EMAIL_API_URL,
        auth=("api", EMAIL_API_KEY),
        data={
            "from": f"{EMAIL_FROM_NAME} <{EMAIL_FROM_ADDRESS}>",
            "to": [to_email],
            "subject": subject,
            "text": text_body,
        },
    )

    print("Email API status:", response.status_code)
    try:
        print("Email API response:", response.json())
    except Exception:
        print("Email API response (raw):", response.text)

    return response.ok


def send_leave_created_email(leave_request):
    """
    Called when an employee creates a new leave request.
    """
    cid = leave_request.cid
    eid = leave_request.eid

    to_email = get_employee_email(cid, eid)
    if not to_email:
        print(
            f"No email configured for cid={cid}, eid={eid}, "
            "skipping 'leave created' notification"
        )
        return False

    employee = Employee.query.filter_by(cid=cid, eid=eid).first()
    if not employee:
        print("Employee not found when sending created email")
        return False

    subject = "Leave request submitted"
    text_body = (
        f"Hi {employee.fname},\n\n"
        f"Your leave request (ID {leave_request.rid}) has been created.\n"
        f"Start date: {leave_request.sdate}\n"
        f"End date: {leave_request.edate}\n"
        f"Type: {leave_request.type}\n"
        f"Status: {leave_request.status}\n\n"
        "Thank you,\n"
        "Leave of Absence Dashboard"
    )

    return send_raw_email(to_email, subject, text_body)


def send_leave_status_update_email(leave_request):
    """
    Called when a manager or admin changes the status of a leave request.
    """
    cid = leave_request.cid
    eid = leave_request.eid

    to_email = get_employee_email(cid, eid)
    if not to_email:
        print(
            f"No email configured for cid={cid}, eid={eid}, "
            "skipping 'status update' notification"
        )
        return False

    employee = Employee.query.filter_by(cid=cid, eid=eid).first()
    if not employee:
        print("Employee not found when sending status update email")
        return False

    subject = "Leave request status updated"
    text_body = (
        f"Hi {employee.fname},\n\n"
        f"Your leave request (ID {leave_request.rid}) has been updated.\n"
        f"New status: {leave_request.status}\n"
        f"Start date: {leave_request.sdate}\n"
        f"End date: {leave_request.edate}\n"
        f"Type: {leave_request.type}\n\n"
        "Thank you,\n"
        "Leave of Absence Dashboard"
    )

    return send_raw_email(to_email, subject, text_body)
