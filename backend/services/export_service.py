import csv
import io
from flask import make_response, send_file
from reportlab.pdfgen import canvas
from models import Employee, LeaveRequest


# Generates a downloadable CSV file containing all employees
def export_employees_csv():
    # String buffer to hold CSV data
    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(["EID", "First Name", "Last Name", "CID", "DID"])

    # Fetch all employee records from the database
    employees = Employee.query.all()

    # Write each employee to the CSV
    for emp in employees:
        writer.writerow([
            emp.eid,
            emp.fname,
            emp.lname,
            emp.cid,
            emp.did
        ])

    # Prepare CSV file response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=employees.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


# Generates a downloadable PDF file containing all leave requests
def export_leave_requests_pdf():
    # Byte buffer for PDF content
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    # PDF title
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 800, "Leave Requests Report")

    y = 770  # vertical position for writing text
    requests = LeaveRequest.query.all()

    # Write each leave request as a line in the PDF
    for req in requests:
        line = (
            f"RID: {req.rid} | EID: {req.eid} | CID: {req.cid} | "
            f"Type: {req.type} | Status: {req.status} | "
            f"Start: {req.sdate} | End: {req.edate}"
        )

        pdf.drawString(50, y, line)
        y -= 20

        # If we reach bottom of page → create new page
        if y < 40:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = 800

    # Finalize PDF
    pdf.save()
    buffer.seek(0)

    # Send PDF file back to user
    return send_file(
        buffer,
        as_attachment=True,
        download_name="leave_requests.pdf",
        mimetype="application/pdf"
    )
