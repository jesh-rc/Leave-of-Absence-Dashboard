from flask import Blueprint, jsonify
from models import LeaveRequest

# Blueprint name MUST match what you register in app.py
ws_bp = Blueprint("ws_bp", __name__)

@ws_bp.route("/export_leave_requests/json", methods=["GET"])
def export_leave_requests_json():
    # Query all leave requests
    requests = LeaveRequest.query.all()

    data = []
    for r in requests:
        data.append({
            "rid": r.rid,
            "eid": r.eid,
            "cid": r.cid,
            "type": r.type,
            "status": r.status,
            "sdate": str(r.sdate),
            "edate": str(r.edate),
            "approvedby": r.approvedby
        })

    # Return JSON structure
    return jsonify({"leave_requests": data})
