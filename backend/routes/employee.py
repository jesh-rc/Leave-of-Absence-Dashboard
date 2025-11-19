# routes/employee.py

from flask import Blueprint, request, jsonify, session
from sqlalchemy import func
from database import db
from models import Employee, UserAccount
from routes.auth_utils import login_required, role_required
from utils.validation import require_fields, ValidationError

employee_bp = Blueprint("employee", __name__)


# ------------------------------------
# (Optional) Get current employee info
# ------------------------------------
@employee_bp.route("/me", methods=["GET"])
@login_required
def get_me():
    cid = session.get("cid")
    eid = session.get("eid")

    emp = Employee.query.filter_by(cid=cid, eid=eid).first()
    if not emp:
        return jsonify({"message": "Employee not found"}), 404

    return jsonify(
        {
            "cid": emp.cid,
            "eid": emp.eid,
            "did": emp.did,
            "fname": emp.fname,
            "lname": emp.lname,
        }
    )


# ------------------------------------
# ADMIN: Create a new employee + login
# POST /employees
#
# Body JSON:
#   {
#     "did": 2,
#     "fname": "Alice",
#     "lname": "Jones",
#     "email": "alice@example.com",
#     "password": "password123"
#   }
#
# cid is taken from the logged-in admin's session
# ------------------------------------
@employee_bp.route("/", methods=["POST"])
@login_required
@role_required("ADMIN")
def create_employee():
    data = request.get_json() or {}

    # We always create employees in the same company as the admin
    cid = session.get("cid")
    if cid is None:
        return jsonify({"message": "Missing company context in session"}), 400

    # Validate required fields
    require_fields(data, ["did", "fname", "lname", "email", "password"])

    try:
        did = int(data["did"])
    except ValueError:
        raise ValidationError("did must be an integer", {"did": data["did"]})

    fname = str(data["fname"]).strip()
    lname = str(data["lname"]).strip()
    email = str(data["email"]).strip()
    password = str(data["password"]).strip()

    if not fname or not lname or not email or not password:
        raise ValidationError(
            "Fields cannot be empty",
            {
                "fname": fname,
                "lname": lname,
                "email": email,
                "password": "(hidden)",
            },
        )

    # Make sure this email/username is not already used in this company
    existing_user = UserAccount.query.filter_by(cid=cid, username=email).first()
    if existing_user:
        raise ValidationError(
            "An account with this email already exists in this company.",
            {"cid": cid, "email": email},
        )

    # Generate a new EID for this company: max(eid) + 1
    max_eid = db.session.query(func.max(Employee.eid)).filter_by(cid=cid).scalar()
    next_eid = (max_eid or 0) + 1

    # Create employee record
    new_emp = Employee(
        eid=next_eid,
        cid=cid,
        did=did,
        fname=fname,
        lname=lname,
    )
    db.session.add(new_emp)

    # Create login account
    # NOTE: In this project we store plain passwords like existing sample_data.
    # In a real app, you MUST hash passwords.
    new_user = UserAccount(
        cid=cid,
        eid=next_eid,
        username=email,
        passhash=password,
    )
    db.session.add(new_user)

    db.session.commit()

    return (
        jsonify(
            {
                "message": "Employee created successfully",
                "employee": {
                    "cid": cid,
                    "eid": next_eid,
                    "did": did,
                    "fname": fname,
                    "lname": lname,
                    "email": email,
                },
            }
        ),
        201,
    )
