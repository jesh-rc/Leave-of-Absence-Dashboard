from flask import Blueprint, request, jsonify
from database import db
from models import Employee
from utils.validation import (
    require_fields,
    ValidationError,
    validate_email,
    ensure_int_in_range,
)
from routes.auth_utils import login_required, role_required

employee_bp = Blueprint('employee', __name__)


# Get all employees (you can leave this open or protect it if you want)
@employee_bp.route('/', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    result = [
        {
            "eid": e.eid,
            "cid": e.cid,
            "did": e.did,
            "fname": e.fname,
            "lname": e.lname,
            "email": getattr(e, "email", None)
        }
        for e in employees
    ]
    return jsonify(result)


# Get specific employee
@employee_bp.route('/<int:cid>/<int:eid>', methods=['GET'])
def get_employee(cid, eid):
    e = Employee.query.filter_by(cid=cid, eid=eid).first()
    if not e:
        return jsonify({"message": "Employee not found"}), 404
    return jsonify({
        "eid": e.eid,
        "cid": e.cid,
        "did": e.did,
        "fname": e.fname,
        "lname": e.lname,
        "email": getattr(e, "email", None)
    })


# Create employee
@employee_bp.route('/', methods=['POST'])
@login_required
@role_required("ADMIN")
def create_employee():
    data = request.get_json() or {}

    try:
        # 1) required fields
        require_fields(data, ["cid", "eid", "fname", "lname", "email"])

        # 2) type + range checks for IDs
        cid = ensure_int_in_range(data["cid"], "cid", min_value=1)
        eid = ensure_int_in_range(data["eid"], "eid", min_value=1)

        # did is optional, but if present make sure it's a positive int
        did = data.get("did")
        if did is not None:
            did = ensure_int_in_range(did, "did", min_value=1)

        # 3) email format
        validate_email(data["email"], "email")

    except ValidationError as ve:
        return jsonify({
            "message": ve.message,
            "details": ve.details
        }), 400

    new_emp = Employee(
        cid=cid,
        eid=eid,
        did=did,
        fname=data["fname"],
        lname=data["lname"],
        email=data["email"],
    )

    db.session.add(new_emp)
    db.session.commit()
    return jsonify({"message": "Employee created!"}), 201


# Update employee
@employee_bp.route('/<int:cid>/<int:eid>', methods=['PUT'])
@login_required
@role_required("ADMIN")
def update_employee(cid, eid):
    e = Employee.query.filter_by(cid=cid, eid=eid).first()
    if not e:
        return jsonify({"message": "Employee not found"}), 404

    data = request.get_json() or {}

    try:
        # optional validation for did and email if they are being updated
        if "did" in data and data["did"] is not None:
            e.did = ensure_int_in_range(data["did"], "did", min_value=1)

        if "email" in data:
            validate_email(data["email"], "email")
            e.email = data["email"]

    except ValidationError as ve:
        return jsonify({
            "message": ve.message,
            "details": ve.details
        }), 400

    e.fname = data.get('fname', e.fname)
    e.lname = data.get('lname', e.lname)

    db.session.commit()
    return jsonify({"message": "Employee updated"})


# Delete employee
@employee_bp.route('/<int:cid>/<int:eid>', methods=['DELETE'])
@login_required
@role_required("ADMIN")
def delete_employee(cid, eid):
    e = Employee.query.filter_by(cid=cid, eid=eid).first()
    if not e:
        return jsonify({"message": "Employee not found"}), 404
    db.session.delete(e)
    db.session.commit()
    return jsonify({"message": "Employee deleted"})
