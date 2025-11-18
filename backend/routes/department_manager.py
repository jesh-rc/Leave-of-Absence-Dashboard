from flask import Blueprint, request, jsonify
from database import db
from models import DepartmentManager

dm_bp = Blueprint('department_manager', __name__)

# List all department managers
@dm_bp.route('/', methods=['GET'])
def get_department_managers():
    managers = DepartmentManager.query.all()
    result = [{"cid": m.cid, "did": m.did, "eid": m.eid} for m in managers]
    return jsonify(result)

# Add a department manager
@dm_bp.route('/', methods=['POST'])
def add_department_manager():
    data = request.get_json()
    new_manager = DepartmentManager(cid=data['cid'], did=data['did'], eid=data['eid'])
    db.session.add(new_manager)
    db.session.commit()
    return jsonify({"message": "Department manager added"})

# Remove a department manager
@dm_bp.route('/<int:cid>/<int:did>', methods=['DELETE'])
def delete_department_manager(cid, did):
    m = DepartmentManager.query.filter_by(cid=cid, did=did).first()
    if not m:
        return jsonify({"message": "Manager not found"}), 404
    db.session.delete(m)
    db.session.commit()
    return jsonify({"message": "Manager removed"})
