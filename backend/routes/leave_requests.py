# routes/leave_requests.py

from flask import Blueprint, request, jsonify, session
from sqlalchemy import text
from database import db
from models import LeaveRequest, Employee, Department
from routes.auth_utils import login_required, role_required
from utils.validation import require_fields, parse_date, ValidationError
from services.email_service import (
    send_leave_created_email,
    send_leave_status_update_email,
)

# Create a Blueprint for leave request routes
leave_bp = Blueprint("leave", __name__)


# ----------------------
# Helper functions: determine roles of an employee
# ----------------------
def is_employee_admin(cid, eid) -> bool:
    sql = text("SELECT 1 FROM company_admin WHERE cid = :cid AND eid = :eid LIMIT 1")
    res = db.session.execute(sql, {"cid": cid, "eid": eid}).first()
    return res is not None


def is_employee_manager(cid, eid) -> bool:
    sql = text(
        "SELECT 1 FROM department_manager WHERE cid = :cid AND eid = :eid LIMIT 1"
    )
    res = db.session.execute(sql, {"cid": cid, "eid": eid}).first()
    return res is not None


# ----------------------
# Get all leave requests
#   - Only ADMIN and MANAGER
#   - Visibility rules:
#       * MANAGER:
#           - Only their own company (cid == session cid)
#           - Can see own requests
#           - Can see employee requests (not admins/managers)
#       * ADMIN:
#           - Can see all companies
#           - Can see own requests
#           - Can see managers and employees
#           - Cannot see other admins
# ----------------------
@leave_bp.route("/", methods=["GET"])
@login_required
@role_required("ADMIN", "MANAGER")
def get_all_leave_requests():
    session_cid = session.get("cid")
    session_eid = session.get("eid")
    role = session.get("role")

    leave_requests = LeaveRequest.query.all()
    result = []

    for lr in leave_requests:
        target_cid = lr.cid
        target_eid = lr.eid

        target_is_admin = is_employee_admin(target_cid, target_eid)
        target_is_manager = is_employee_manager(target_cid, target_eid)

        # ---- MANAGER visibility rules ----
        if role == "MANAGER":
            # Managers only see their own company
            if target_cid != session_cid:
                continue

            # Always allowed to see their own requests
            if not (target_cid == session_cid and target_eid == session_eid):
                # For other people in their company: only employees
                if target_is_admin or target_is_manager:
                    continue

        # ---- ADMIN visibility rules ----
        elif role == "ADMIN":
            # Admins can see all companies
            # But they cannot see *other* admins (only themselves as admin)
            if target_is_admin and not (
                target_cid == session_cid and target_eid == session_eid
            ):
                continue

        employee = Employee.query.filter_by(eid=lr.eid, cid=lr.cid).first()

        dept_id = None
        dept_name = None
        if employee:
            dept_id = employee.did
            dept = Department.query.filter_by(
                cid=employee.cid, did=employee.did
            ).first()
            if dept:
                dept_name = dept.dname

        # 🔹 Lookup approver name (if any)
        approver_name = None
        if lr.approvedby is not None:
            approver_emp = Employee.query.filter_by(
                eid=lr.approvedby, cid=lr.cid
            ).first()
            if approver_emp:
                approver_name = f"{approver_emp.fname} {approver_emp.lname}"

        result.append(
            {
                "rid": lr.rid,
                "eid": lr.eid,
                "employee_name": f"{employee.fname} {employee.lname}"
                if employee
                else None,
                "cid": lr.cid,
                "department_id": dept_id,
                "department_name": dept_name,
                "start_date": lr.sdate.isoformat(),
                "end_date": lr.edate.isoformat(),
                "type": lr.type,
                "status": lr.status,
                # 🔹 Keep EID for compatibility, add human name too
                "approved_by": lr.approvedby,
                "approved_by_name": approver_name,
                "created_at": lr.createdat.isoformat(),
            }
        )

    return jsonify(result)


# ----------------------
# Get leave requests by employee
#   - EMPLOYEE: only their own
#   - ADMIN/MANAGER: can see anyone (subject to general rules if you later extend)
# ----------------------
@leave_bp.route("/employee/<int:cid>/<int:eid>", methods=["GET"])
@login_required
def get_leave_by_employee(cid, eid):
    session_cid = session.get("cid")
    session_eid = session.get("eid")
    role = session.get("role")

    # If not admin/manager, only allow user to see their own
    if role not in ("ADMIN", "MANAGER"):
        if cid != session_cid or eid != session_eid:
            return (
                jsonify({"message": "Forbidden: cannot view other employees' leave"}),
                403,
            )

    leave_requests = LeaveRequest.query.filter_by(cid=cid, eid=eid).all()
    result = []
    for lr in leave_requests:
        approver_name = None
        if lr.approvedby is not None:
            approver_emp = Employee.query.filter_by(
                eid=lr.approvedby, cid=lr.cid
            ).first()
            if approver_emp:
                approver_name = f"{approver_emp.fname} {approver_emp.lname}"

        result.append(
            {
                "rid": lr.rid,
                "start_date": lr.sdate.isoformat(),
                "end_date": lr.edate.isoformat(),
                "type": lr.type,
                "status": lr.status,
                "approved_by": lr.approvedby,
                "approved_by_name": approver_name,
                "created_at": lr.createdat.isoformat(),
            }
        )
    return jsonify(result)


# ----------------------
# Create a new leave request
#   - must be logged in; use session cid/eid
# ----------------------
@leave_bp.route("/", methods=["POST"])
@login_required
def create_leave_request():
    data = request.get_json() or {}

    cid = session.get("cid")
    eid = session.get("eid")

    # Let ValidationError bubble to the global handler
    require_fields(data, ["sdate", "edate", "type"])
    sdate = parse_date(data["sdate"], "sdate")
    edate = parse_date(data["edate"], "edate")

    days = (edate - sdate).days + 1
    if days <= 0:
        raise ValidationError(
            "Leave days must be greater than 0",
            {"sdate": data["sdate"], "edate": data["edate"], "days": days},
        )

    # ---- Normalize leave type to match Postgres enum ----
    raw_type = data.get("type", "Vacation")
    key = str(raw_type).strip().lower()

    type_map = {
        "vacation": "Vacation",
        "personal": "Personal",
        "sick": "Sick",
    }

    if key not in type_map:
        # If someone sends a totally invalid type, treat it as a validation error
        raise ValidationError(
            "Invalid leave type",
            {"allowed_values": list(type_map.values()), "received": raw_type},
        )

    leavetype = type_map[key]

    new_request = LeaveRequest(
        eid=eid,
        cid=cid,
        sdate=sdate,
        edate=edate,
        type=leavetype,  # matches enum: 'Vacation', 'Personal', or 'Sick'
        status="Pending",
        approvedby=None,
    )
    db.session.add(new_request)
    db.session.commit()

    # send notification email to employee, if configured
    try:
        send_leave_created_email(new_request)
    except Exception as e:
        # do not break the app if email fails
        print("Error sending leave created email:", e)

    return jsonify({"message": "Leave request created!"}), 201


# ----------------------
# Update a leave request (approve/decline)
#   - Only ADMIN or MANAGER
#   - Additional rules:
#       * MANAGER:
#           - Only their own company (cid == session cid)
#           - Cannot approve/reject admins or managers (except themselves)
#       * ADMIN:
#           - Cannot approve/reject other admins (only their own requests)
# ----------------------
@leave_bp.route("/<int:rid>", methods=["PUT"])
@login_required
@role_required("ADMIN", "MANAGER")
def update_leave_request(rid):
    data = request.get_json() or {}
    lr = LeaveRequest.query.get(rid)
    if not lr:
        return jsonify({"message": "Leave request not found"}), 404

    session_cid = session.get("cid")
    session_eid = session.get("eid")
    role = session.get("role")

    target_cid = lr.cid
    target_eid = lr.eid

    target_is_admin = is_employee_admin(target_cid, target_eid)
    target_is_manager = is_employee_manager(target_cid, target_eid)

    # ---- MANAGER rules ----
    if role == "MANAGER":
        # Only own company
        if target_cid != session_cid:
            return (
                jsonify(
                    {"message": "Forbidden: cannot update other companies' requests"}
                ),
                403,
            )

        # Cannot act on admins or managers (except possibly themselves)
        if (target_is_admin or target_is_manager) and not (
            target_cid == session_cid and target_eid == session_eid
        ):
            return (
                jsonify(
                    {
                        "message": "Forbidden: cannot update admin/manager requests"
                    }
                ),
                403,
            )

    # ---- ADMIN rules ----
    if role == "ADMIN":
        # Cannot act on *other* admins (but can act on themselves)
        if target_is_admin and not (
            target_cid == session_cid and target_eid == session_eid
        ):
            return (
                jsonify(
                    {"message": "Forbidden: cannot update other admins' requests"}
                ),
                403,
            )

    try:
        # optional validation for status
        if "status" in data:
            allowed_status = {"Pending", "Approved", "Rejected"}
            status = data["status"]
            if status not in allowed_status:
                raise ValidationError(
                    "Invalid status value",
                    {"allowed_values": list(allowed_status), "received": status},
                )
            lr.status = status

        if "approvedby" in data:
            if data["approvedby"] is not None and not str(
                data["approvedby"]
            ).strip():
                raise ValidationError(
                    "approvedby cannot be empty string",
                    {"approvedby": data["approvedby"]},
                )
            lr.approvedby = data["approvedby"]

    except ValidationError as ve:
        return (
            jsonify(
                {
                    "message": ve.message,
                    "details": ve.details,
                }
            ),
            400,
        )

    db.session.commit()

    # after updating, send notification about new status
    try:
        send_leave_status_update_email(lr)
    except Exception as e:
        print("Error sending status update email:", e)

    return jsonify({"message": "Leave request updated!"})


# ----------------------
# Delete a leave request
#   - ADMIN/MANAGER: any (you can tighten this if you want)
#   - EMPLOYEE: only their own
# ----------------------
@leave_bp.route("/<int:rid>", methods=["DELETE"])
@login_required
def delete_leave_request(rid):
    lr = LeaveRequest.query.get(rid)
    if not lr:
        return jsonify({"message": "Leave request not found"}), 404

    session_cid = session.get("cid")
    session_eid = session.get("eid")
    role = session.get("role")

    # ADMIN / MANAGER can delete anything (currently)
    if role not in ("ADMIN", "MANAGER"):
        # EMPLOYEE: only own request
        if lr.cid != session_cid or lr.eid != session_eid:
            return jsonify({"message": "Forbidden: cannot delete others' requests"}), 403

    db.session.delete(lr)
    db.session.commit()
    return jsonify({"message": "Leave request deleted"})
