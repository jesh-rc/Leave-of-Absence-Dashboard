from database import db
from sqlalchemy.sql import func
from sqlalchemy import Enum

LEAVE_TYPES = ('Vacation', 'Personal', 'Sick')

# --------------------
# Company table
# --------------------
class Company(db.Model):
    __tablename__ = "company"
    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


# --------------------
# Department table
# --------------------
class Department(db.Model):
    __tablename__ = "department"
    did = db.Column(db.Integer, nullable=False)
    cid = db.Column(db.Integer, nullable=False)
    dname = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("did", "cid"),
        db.ForeignKeyConstraint(["cid"], ["company.cid"]),
    )


# --------------------
# Employee table
# --------------------
class Employee(db.Model):
    __tablename__ = "employee"
    eid = db.Column(db.Integer, nullable=False)
    cid = db.Column(db.Integer, nullable=False)
    did = db.Column(db.Integer, nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("eid", "cid"),
        db.ForeignKeyConstraint(["cid"], ["company.cid"]),
        db.ForeignKeyConstraint(["did", "cid"], ["department.did", "department.cid"]),
    )


# --------------------
# DepartmentManager table
# --------------------
class DepartmentManager(db.Model):
    __tablename__ = "department_manager"
    cid = db.Column(db.Integer, nullable=False)
    did = db.Column(db.Integer, nullable=False)
    eid = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("cid", "did"),
        db.ForeignKeyConstraint(["cid", "did"], ["department.cid", "department.did"]),
        db.ForeignKeyConstraint(["cid", "eid"], ["employee.cid", "employee.eid"]),
    )


# --------------------
# CompanyAdmin table
# --------------------
class CompanyAdmin(db.Model):
    __tablename__ = "company_admin"
    cid = db.Column(db.Integer, nullable=False)
    eid = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("cid", "eid"),
        db.ForeignKeyConstraint(["cid", "eid"], ["employee.cid", "employee.eid"]),
    )


# --------------------
# LeaveBalance table
# --------------------
class LeaveBalance(db.Model):
    __tablename__ = "leave_balance"
    cid = db.Column(db.Integer, nullable=False)
    eid = db.Column(db.Integer, nullable=False)
    leavetype = db.Column(Enum(*LEAVE_TYPES, name="leave_type_enum"), nullable=False)
    totaldays = db.Column(db.Integer, nullable=False)
    useddays = db.Column(db.Integer, default=0)
    remainingdays = db.Column(db.Integer, default=0)

    __table_args__ = (
        db.PrimaryKeyConstraint("cid", "eid", "leavetype"),
        db.ForeignKeyConstraint(["cid", "eid"], ["employee.cid", "employee.eid"]),
    )


# --------------------
# LeaveRequest table
# --------------------
class LeaveRequest(db.Model):
    __tablename__ = "leaverequest"
    rid = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.Integer, nullable=False)
    cid = db.Column(db.Integer, nullable=False)
    sdate = db.Column(db.Date, nullable=False)
    edate = db.Column(db.Date, nullable=False)
    type = db.Column(Enum(*LEAVE_TYPES, name="leave_type_enum"), nullable=False)
    status = db.Column(db.String(20), default="Pending", nullable=False)
    approvedby = db.Column(db.Integer, nullable=True)
    createdat = db.Column(db.DateTime, server_default=func.current_timestamp(), nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint(["cid", "eid"], ["employee.cid", "employee.eid"]),
    )


# --------------------
# UserAccount table
# --------------------
class UserAccount(db.Model):
    __tablename__ = "user_account"
    cid = db.Column(db.Integer, nullable=False)
    eid = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    passhash = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("cid", "eid"),
        db.ForeignKeyConstraint(["cid", "eid"], ["employee.cid", "employee.eid"]),
    )
