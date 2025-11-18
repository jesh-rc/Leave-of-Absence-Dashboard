import csv
import io
from flask import make_response, send_file
from reportlab.pdfgen import canvas
from models import Employee, LeaveRequest

def export_employees_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["EID", "First Name", "Last Name", "CID", "DID"])

    employees = Employee.query.all()
    for emp in employees:
        writer.writerow([
            emp.eid,
            emp.fname,
            emp.lname,
            emp.cid,
            emp.did
        ])

    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=employees.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


def export_leave_requests_pdf():
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 800, "Leave Requests Report")

    y = 770
    requests = LeaveRequest.query.all()

    for req in requests:
        line = (
            f"RID: {req.rid} | "
            f"EID: {req.eid} | "
            f"CID: {req.cid} | "
            f"Type: {req.type} | "
            f"Status: {req.status} | "
            f"Start: {req.sdate} | "
            f"End: {req.edate}"
        )

        pdf.drawString(50, y, line)
        y -= 20

        if y < 40:
            pdf.showPage()
            y = 800

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="leave_requests.pdf",
        mimetype="application/pdf"
    )
