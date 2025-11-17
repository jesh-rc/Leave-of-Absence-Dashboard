from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import UserAccount

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# ----------------------
# Login route
# ----------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    user = UserAccount.query.filter_by(username=username).first()
    if user and check_password_hash(user.passhash, password):
        session['cid'] = user.cid
        session['eid'] = user.eid
        return jsonify({"message": "Login successful!"})
    return jsonify({"message": "Invalid username or password"}), 401

# ----------------------
# Logout route
# ----------------------
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully!"})

# ----------------------
# Optional: Register route
# ----------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
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

    return jsonify({"message": "User registered successfully!"})
