# leave_requests.py
from flask import Blueprint, request, jsonify, session
from app import db
from models import LeaveRequest, Employee

# Create a Blueprint for leave request routes
leave_bp = Blueprint('leave', __name__)

# ----------------------
# Get all leave requests
# ----------------------
@leave_bp.route('/', methods=['GET'])
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
# ----------------------
@leave_bp.route('/employee/<int:cid>/<int:eid>', methods=['GET'])
def get_leave_by_employee(cid, eid):
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
# ----------------------
@leave_bp.route('/', methods=['POST'])
def create_leave_request():
    data = request.get_json()
    new_request = LeaveRequest(
        eid=data['eid'],
        cid=data['cid'],
        sdate=data['sdate'],
        edate=data['edate'],
        type=data['type'],
        status=data.get('status', 'Pending'),
        approvedby=data.get('approvedby')
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Leave request created!"})

# ----------------------
# Update a leave request (approve/decline)
# ----------------------
@leave_bp.route('/<int:rid>', methods=['PUT'])
def update_leave_request(rid):
    data = request.get_json()
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
# ----------------------
@leave_bp.route('/<int:rid>', methods=['DELETE'])
def delete_leave_request(rid):
    lr = LeaveRequest.query.get(rid)
    if not lr:
        return jsonify({"message": "Leave request not found"}), 404
    db.session.delete(lr)
    db.session.commit()
    return jsonify({"message": "Leave request deleted!"})
