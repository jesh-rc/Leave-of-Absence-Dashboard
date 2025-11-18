from flask import Blueprint, request, jsonify
from database import db
from models import Employee

employee_bp = Blueprint('employee', __name__)

# Get all employees
@employee_bp.route('/', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    result = [{"eid": e.eid, "cid": e.cid, "did": e.did, "fname": e.fname, "lname": e.lname} for e in employees]
    return jsonify(result)

# Get specific employee
@employee_bp.route('/<int:cid>/<int:eid>', methods=['GET'])
def get_employee(cid, eid):
    e = Employee.query.filter_by(cid=cid, eid=eid).first()
    if not e:
        return jsonify({"message": "Employee not found"}), 404
    return jsonify({"eid": e.eid, "cid": e.cid, "did": e.did, "fname": e.fname, "lname": e.lname})

# Create employee
@employee_bp.route('/', methods=['POST'])
def create_employee():
    data = request.get_json()
    new_employee = Employee(cid=data['cid'], eid=data['eid'], did=data['did'], fname=data['fname'], lname=data['lname'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"message": "Employee created"})

# Update employee
@employee_bp.route('/<int:cid>/<int:eid>', methods=['PUT'])
def update_employee(cid, eid):
    e = Employee.query.filter_by(cid=cid, eid=eid).first()
    if not e:
        return jsonify({"message": "Employee not found"}), 404
    data = request.get_json()
    e.fname = data.get('fname', e.fname)
    e.lname = data.get('lname', e.lname)
    e.did = data.get('did', e.did)
    db.session.commit()
    return jsonify({"message": "Employee updated"})

# Delete employee
@employee_bp.route('/<int:cid>/<int:eid>', methods=['DELETE'])
def delete_employee(cid, eid):
    e = Employee.query.filter_by(cid=cid, eid=eid).first()
    if not e:
        return jsonify({"message": "Employee not found"}), 404
    db.session.delete(e)
    db.session.commit()
    return jsonify({"message": "Employee deleted"})
