from flask import Blueprint
from services.export_service import export_employees_csv, export_leave_requests_pdf

export_bp = Blueprint("export", __name__)

@export_bp.route("/employees/csv", methods=["GET"])
def export_employees():
    
    # Calls the service function to generate and return a CSV file
    return export_employees_csv()

@export_bp.route("/leave_requests/pdf", methods=["GET"])
def export_leave_requests():
    
     # Calls the service function to generate and return a PDF file
    return export_leave_requests_pdf()
