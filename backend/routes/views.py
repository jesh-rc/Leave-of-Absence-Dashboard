from flask import Blueprint, jsonify
from sqlalchemy import text
from database import db

views_bp = Blueprint("views", __name__)

# Allow only view1 ... view10 to be queried
VALID_VIEWS = {f"view{i}": f"view{i}" for i in range(1, 11)}

@views_bp.get("/<view_name>")
def get_view(view_name):
    if view_name not in VALID_VIEWS:
        return jsonify({"error": "Unknown view"}), 404

    sql = text(f"SELECT * FROM {VALID_VIEWS[view_name]}")
    result = db.session.execute(sql)
    rows = [dict(row._mapping) for row in result]
    return jsonify(rows)
