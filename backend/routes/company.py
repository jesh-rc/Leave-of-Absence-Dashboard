from flask import Blueprint, request, jsonify
from database import db
from models import Company

company_bp = Blueprint('company', __name__)

# Get all companies
@company_bp.route('/', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    result = [{"cid": c.cid, "name": c.name} for c in companies]
    return jsonify(result)

# Get a specific company
@company_bp.route('/<int:cid>', methods=['GET'])
def get_company(cid):
    c = Company.query.get(cid)
    if not c:
        return jsonify({"message": "Company not found"}), 404
    return jsonify({"cid": c.cid, "name": c.name})

# Create a new company
@company_bp.route('/', methods=['POST'])
def create_company():
    data = request.get_json()
    new_company = Company(name=data['name'])
    db.session.add(new_company)
    db.session.commit()
    return jsonify({"message": "Company created", "cid": new_company.cid})

# Update a company
@company_bp.route('/<int:cid>', methods=['PUT'])
def update_company(cid):
    data = request.get_json()
    c = Company.query.get(cid)
    if not c:
        return jsonify({"message": "Company not found"}), 404
    c.name = data.get('name', c.name)
    db.session.commit()
    return jsonify({"message": "Company updated"})

# Delete a company
@company_bp.route('/<int:cid>', methods=['DELETE'])
def delete_company(cid):
    c = Company.query.get(cid)
    if not c:
        return jsonify({"message": "Company not found"}), 404
    db.session.delete(c)
    db.session.commit()
    return jsonify({"message": "Company deleted"})
