from flask import Blueprint, request, jsonify
from database import db
from models import Department

department_bp = Blueprint('department', __name__)

# Get all departments
@department_bp.route('/', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    result = [{"cid": d.cid, "did": d.did, "dname": d.dname} for d in departments]
    return jsonify(result)

# Get specific department
@department_bp.route('/<int:cid>/<int:did>', methods=['GET'])
def get_department(cid, did):
    d = Department.query.filter_by(cid=cid, did=did).first()
    if not d:
        return jsonify({"message": "Department not found"}), 404
    return jsonify({"cid": d.cid, "did": d.did, "dname": d.dname})

# Create department
@department_bp.route('/', methods=['POST'])
def create_department():
    data = request.get_json()
    new_department = Department(cid=data['cid'], did=data['did'], dname=data['dname'])
    db.session.add(new_department)
    db.session.commit()
    return jsonify({"message": "Department created"})

# Update department
@department_bp.route('/<int:cid>/<int:did>', methods=['PUT'])
def update_department(cid, did):
    d = Department.query.filter_by(cid=cid, did=did).first()
    if not d:
        return jsonify({"message": "Department not found"}), 404
    data = request.get_json()
    d.dname = data.get('dname', d.dname)
    db.session.commit()
    return jsonify({"message": "Department updated"})

# Delete department
@department_bp.route('/<int:cid>/<int:did>', methods=['DELETE'])
def delete_department(cid, did):
    d = Department.query.filter_by(cid=cid, did=did).first()
    if not d:
        return jsonify({"message": "Department not found"}), 404
    db.session.delete(d)
    db.session.commit()
    return jsonify({"message": "Department deleted"})
