from app import db
from sqlalchemy.sql import func

# --------------------
# Company table
# --------------------
class Company(db.Model):
    __tablename__ = "company"

    Cid = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    AdminID = db.Column(db.Integer, db.ForeignKey("employee.Eid"), nullable=False)

# --------------------
# Department table (composite PK: Did + Cid)
# --------------------
class Department(db.Model):
    __tablename__ = "department"

    Did = db.Column(db.Integer, nullable=False)
    Cid = db.Column(db.Integer, db.ForeignKey("company.Cid"), nullable=False)
    Dname = db.Column(db.String(100), nullable=False)
    ManagerID = db.Column(db.Integer, db.ForeignKey("employee.Eid"), nullable=True)

    __table_args__ = (
        db.PrimaryKeyConstraint("Did", "Cid"),
    )

# --------------------
# Employee table (composite PK: Eid + Cid)
# --------------------
class Employee(db.Model):
    __tablename__ = "employee"

    Eid = db.Column(db.Integer, nullable=False)
    Cid = db.Column(db.Integer, db.ForeignKey("company.Cid"), nullable=False)
    Did = db.Column(db.Integer, db.ForeignKey("department.Did"), nullable=False)
    Sid = db.Column(db.Integer, db.ForeignKey("employee.Eid"), nullable=True)
    Fname = db.Column(db.String(50), nullable=False)
    Lname = db.Column(db.String(50), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("Eid", "Cid"),
    )

# --------------------
# LeaveRequest table (composite PK: Rid + Eid)
# --------------------
class LeaveRequest(db.Model):
    __tablename__ = "leave_request"

    Rid = db.Column(db.Integer, nullable=False)
    Eid = db.Column(db.Integer, db.ForeignKey("employee.Eid"), nullable=False)
    Cid = db.Column(db.Integer, db.ForeignKey("company.Cid"), nullable=False)
    Sdate = db.Column(db.Date, nullable=False)
    Edate = db.Column(db.Date, nullable=False)
    Reason = db.Column(db.Text, nullable=True)  # This maps to LeaveType in LeaveBalance
    Status = db.Column(db.String(20), default="Pending")
    ApprovedBy = db.Column(db.Integer, db.ForeignKey("employee.Eid"), nullable=True)
    CreatedAt = db.Column(db.DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        db.PrimaryKeyConstraint("Rid", "Eid"),
    )

# --------------------
# LeaveBalance table (composite PK: Cid + Eid + LeaveType)
# --------------------
class LeaveBalance(db.Model):
    __tablename__ = "leave_balance"

    Cid = db.Column(db.Integer, db.ForeignKey("company.Cid"), nullable=False)
    Eid = db.Column(db.Integer, db.ForeignKey("employee.Eid"), nullable=False)
    LeaveType = db.Column(db.String(50), nullable=False)  # Matches LeaveRequest.Reason
    TotalDays = db.Column(db.Integer, nullable=False)
    UsedDays = db.Column(db.Integer, default=0)
    RemainingDays = db.Column(db.Integer, default=0)

    __table_args__ = (
        db.PrimaryKeyConstraint("Cid", "Eid", "LeaveType"),
    )

# --------------------
# UserAccount table (composite PK: Cid + Eid)
# --------------------
class UserAccount(db.Model):
    __tablename__ = "user_account"

    Cid = db.Column(db.Integer, db.ForeignKey("company.Cid"), nullable=False)
    Eid = db.Column(db.Integer, db.ForeignKey("employee.Eid"), nullable=False)
    User = db.Column(db.String(50), nullable=False)
    PassHash = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("Cid", "Eid"),
    )
