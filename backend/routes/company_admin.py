from flask import Blueprint, request, jsonify
from app import db
from models import CompanyAdmin

ca_bp = Blueprint('company_admin', __name__)

# List all admins
@ca_bp.route('/', methods=['GET'])
def get_admins():
    admins = CompanyAdmin.query.all()
    result = [{"cid": a.cid, "eid": a.eid} for a in admins]
    return jsonify(result)

# Add an admin
@ca_bp.route('/', methods=['POST'])
def add_admin():
    data = request.get_json()
    new_admin = CompanyAdmin(cid=data['cid'], eid=data['eid'])
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({"message": "Admin added"})

# Remove an admin
@ca_bp.route('/<int:cid>/<int:eid>', methods=['DELETE'])
def delete_admin(cid, eid):
    a = CompanyAdmin.query.filter_by(cid=cid, eid=eid).first()
    if not a:
        return jsonify({"message": "Admin not found"}), 404
    db.session.delete(a)
    db.session.commit()
    return jsonify({"message": "Admin removed"})
