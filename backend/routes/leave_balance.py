from flask import Blueprint, request, jsonify
from database import db
from models import LeaveBalance

lb_bp = Blueprint('leave_balance', __name__)

# Get leave balances for an employee
@lb_bp.route('/<int:cid>/<int:eid>', methods=['GET'])
def get_leave_balance(cid, eid):
    balances = LeaveBalance.query.filter_by(cid=cid, eid=eid).all()
    result = [{"leavetype": b.leavetype, "totaldays": b.totaldays, "useddays": b.useddays, "remainingdays": b.remainingdays} for b in balances]
    return jsonify(result)

# Add leave balance
@lb_bp.route('/', methods=['POST'])
def add_leave_balance():
    data = request.get_json()
    new_balance = LeaveBalance(cid=data['cid'], eid=data['eid'], leavetype=data['leavetype'], totaldays=data['totaldays'], useddays=data.get('useddays', 0), remainingdays=data.get('remainingdays', 0))
    db.session.add(new_balance)
    db.session.commit()
    return jsonify({"message": "Leave balance added"})

# Update leave balance
@lb_bp.route('/<int:cid>/<int:eid>/<leavetype>', methods=['PUT'])
def update_leave_balance(cid, eid, leavetype):
    b = LeaveBalance.query.filter_by(cid=cid, eid=eid, leavetype=leavetype).first()
    if not b:
        return jsonify({"message": "Leave balance not found"}), 404
    data = request.get_json()
    b.totaldays = data.get('totaldays', b.totaldays)
    b.useddays = data.get('useddays', b.useddays)
    b.remainingdays = data.get('remainingdays', b.remainingdays)
    db.session.commit()
    return jsonify({"message": "Leave balance updated"})

# Delete leave balance
@lb_bp.route('/<int:cid>/<int:eid>/<leavetype>', methods=['DELETE'])
def delete_leave_balance(cid, eid, leavetype):
    b = LeaveBalance.query.filter_by(cid=cid, eid=eid, leavetype=leavetype).first()
    if not b:
        return jsonify({"message": "Leave balance not found"}), 404
    db.session.delete(b)
    db.session.commit()
    return jsonify({"message": "Leave balance deleted"})
