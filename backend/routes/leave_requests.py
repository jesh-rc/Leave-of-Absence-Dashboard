# routes/leave_requests.py

from flask import Blueprint, request, jsonify, session
from database import db
from models import LeaveRequest, Employee
from routes.auth_utils import login_required, role_required

# Create a Blueprint for leave request routes
leave_bp = Blueprint('leave', __name__)


# ----------------------
# Get all leave requests
#   - Only ADMIN and MANAGER
# ----------------------
@leave_bp.route('/', methods=['GET'])
@login_required
@role_required("ADMIN", "MANAGER")
def get_all_leave_requests():
    leave_requests = LeaveRequest.query.all()
    result = []
    for lr in leave_requests:
        employee = Employee.query.filter_by(eid=lr.eid, cid=lr.cid).first()
        result.append({
            "rid": lr.rid,
            "eid": lr.eid,
            "employee_name": f"{employee.fname} {employee.lname}" if employee else None,
            "cid": lr.cid,
            "start_date": lr.sdate.isoformat(),
            "end_date": lr.edate.isoformat(),
            "type": lr.type,
            "status": lr.status,
            "approved_by": lr.approvedby,
            "created_at": lr.createdat.isoformat()
        })
    return jsonify(result)


# ----------------------
# Get leave requests by employee
#   - EMPLOYEE: only their own
#   - ADMIN/MANAGER: can see anyone
# ----------------------
@leave_bp.route('/employee/<int:cid>/<int:eid>', methods=['GET'])
@login_required
def get_leave_by_employee(cid, eid):
    session_cid = session.get("cid")
    session_eid = session.get("eid")
    role = session.get("role")

    # If not admin/manager, only allow user to see their own
    if role not in ("ADMIN", "MANAGER"):
        if cid != session_cid or eid != session_eid:
            return jsonify({"message": "Forbidden: cannot view other employees' leave"}), 403

    leave_requests = LeaveRequest.query.filter_by(cid=cid, eid=eid).all()
    result = []
    for lr in leave_requests:
        result.append({
            "rid": lr.rid,
            "start_date": lr.sdate.isoformat(),
            "end_date": lr.edate.isoformat(),
            "type": lr.type,
            "status": lr.status,
            "approved_by": lr.approvedby,
            "created_at": lr.createdat.isoformat()
        })
    return jsonify(result)


# ----------------------
# Create a new leave request
#   - must be logged in; use session cid/eid
# ----------------------
@leave_bp.route('/', methods=['POST'])
@login_required
def create_leave_request():
    data = request.get_json() or {}

    cid = session.get("cid")
    eid = session.get("eid")

    sdate = data.get('sdate')
    edate = data.get('edate')
    leavetype = data.get('type')

    if not sdate or not edate or not leavetype:
        return jsonify({"message": "sdate, edate, and type are required"}), 400

    new_request = LeaveRequest(
        eid=eid,
        cid=cid,
        sdate=sdate,
        edate=edate,
        type=leavetype,
        status='Pending',
        approvedby=None
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Leave request created!"}), 201


# ----------------------
# Update a leave request (approve/decline)
#   - Only ADMIN or MANAGER
# ----------------------
@leave_bp.route('/<int:rid>', methods=['PUT'])
@login_required
@role_required("ADMIN", "MANAGER")
def update_leave_request(rid):
    data = request.get_json() or {}
    lr = LeaveRequest.query.get(rid)
    if not lr:
        return jsonify({"message": "Leave request not found"}), 404

    if 'status' in data:
        lr.status = data['status']
    if 'approvedby' in data:
        lr.approvedby = data['approvedby']

    db.session.commit()
    return jsonify({"message": "Leave request updated!"})


# ----------------------
# Delete a leave request
#   - ADMIN/MANAGER: any
#   - EMPLOYEE: only their own
# ----------------------
@leave_bp.route('/<int:rid>', methods=['DELETE'])
@login_required
def delete_leave_request(rid):
    lr = LeaveRequest.query.get(rid)
    if not lr:
        return jsonify({"message": "Leave request not found"}), 404

    session_cid = session.get("cid")
    session_eid = session.get("eid")
    role = session.get("role")

    # ADMIN / MANAGER can delete anything
    if role not in ("ADMIN", "MANAGER"):
        # EMPLOYEE: only own request
        if lr.cid != session_cid or lr.eid != session_eid:
            return jsonify({"message": "Forbidden: cannot delete others' requests"}), 403

    db.session.delete(lr)
    db.session.commit()
    return jsonify({"message": "Leave request deleted"})
