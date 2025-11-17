from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import UserAccount, CompanyAdmin, DepartmentManager

auth_bp = Blueprint('auth', __name__)


def get_user_role(cid: int, eid: int) -> str:
    """Return 'ADMIN', 'MANAGER', or 'EMPLOYEE' for this user."""
    admin = CompanyAdmin.query.filter_by(cid=cid, eid=eid).first()
    if admin:
        return "ADMIN"

    manager = DepartmentManager.query.filter_by(cid=cid, eid=eid).first()
    if manager:
        return "MANAGER"

    return "EMPLOYEE"


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    # 1) basic validation
    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    # 2) lookup user
    user = UserAccount.query.filter_by(username=username).first()
    if not user:
        # username not found
        return jsonify({"message": "Invalid username or password"}), 401

    # 3) password check
    # sample_data.sql might store plaintext "password" for dev users.
    # So accept either a real hash or a raw 'password'.
    if not (check_password_hash(user.passhash, password) or user.passhash == "password"):
        return jsonify({"message": "Invalid username or password"}), 401

    # 4) figure out role from company_admin / department_manager tables
    role = get_user_role(user.cid, user.eid)

    # 5) store info in session
    session['cid'] = user.cid
    session['eid'] = user.eid
    session['username'] = user.username
    session['role'] = role

    # 6) return info to frontend
    return jsonify({
        "message": "Login successful!",
        "cid": user.cid,
        "eid": user.eid,
        "username": user.username,
        "role": role
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully!"})


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    cid = data.get('cid')
    eid = data.get('eid')

    if not username or not password or not cid or not eid:
        return jsonify({"message": "All fields are required"}), 400

    existing_user = UserAccount.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = UserAccount(
        cid=cid,
        eid=eid,
        username=username,
        passhash=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201
