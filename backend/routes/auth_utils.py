# routes/auth_utils.py
from functools import wraps
from flask import session, jsonify


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'cid' not in session or 'eid' not in session or 'role' not in session:
            return jsonify({"message": "Authentication required"}), 401
        return fn(*args, **kwargs)
    return wrapper


def role_required(*allowed_roles):
    """
    Example:
        @role_required("ADMIN")
        @role_required("ADMIN", "MANAGER")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            role = session.get("role")
            if role is None:
                return jsonify({"message": "Authentication required"}), 401
            if role not in allowed_roles:
                return jsonify({
                    "message": "Forbidden",
                    "required_roles": allowed_roles
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
