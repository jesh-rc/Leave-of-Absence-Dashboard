from app import db
from sqlalchemy.sql import func
from sqlalchemy import Enum

"""

This file defines the database models for a company employee management system using Flask-SQLAlchemy.

It tells Flask-SQLAlchemy how to structure the database tables, including columns, primary keys, composite keys, and relationships between tables.
Each class represents a table, and each attribute of the class represents a column in that table.

This file also enforces the relationships between tables, such as foreign keys and constraints, ensuring data integrity.
Without this file, Flask-SQLAlchemy wouldn’t know how to create, query, or update the database, and the backend application would not be able to interact with the database correctly.

"""
# --------------------
# Company table
# --------------------
class Company(db.Model):
    __tablename__ = "company"

    # Columns
    Cid = db.Column(db.Integer, primary_key=True)  # Company ID
    Name = db.Column(db.String(100), nullable=False)  # Company name
    AdminID = db.Column(db.Integer, nullable=False)  # Admin's Employee ID

    __table_args__ = (
        db.ForeignKeyConstraint(["AdminID", "Cid"], ["employee.Eid", "employee.Cid"]),
    )

# --------------------
# Employee table (composite PK: Eid + Cid)
# --------------------
class Employee(db.Model):
    __tablename__ = "employee"

    # Columns
    Eid = db.Column(db.Integer, nullable=False)  # Employee ID
    Cid = db.Column(db.Integer, db.ForeignKey("company.Cid"), nullable=False)  # Company ID
    Did = db.Column(db.Integer, db.ForeignKey("department.Did"), nullable=False)  # Department ID
    Fname = db.Column(db.String(50), nullable=False)
    Lname = db.Column(db.String(50), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("Eid", "Cid"),
        db.ForeignKeyConstraint(
            ["Did", "Cid"], ["department.Did", "department.Cid"]
        ),
    )


# --------------------
# Department table (composite PK: Did + Cid)
# --------------------
class Department(db.Model):
    __tablename__ = "department"

    # Columns
    Did = db.Column(db.Integer, nullable=False)   # Department ID
    Cid = db.Column(db.Integer, db.ForeignKey("company.Cid"), nullable=False)  # Company ID
    Dname = db.Column(db.String(100), nullable=False)  # Department name
    ManagerID = db.Column(db.Integer, nullable=True)   # Manager’s Employee ID

    __table_args__ = (
        db.PrimaryKeyConstraint("Did", "Cid"),
        db.ForeignKeyConstraint(
            ["ManagerID", "Cid"], ["employee.Eid", "employee.Cid"]
        ),
    )


# --------------------
# LeaveRequest table (PK: Rid)
# --------------------

LEAVE_TYPES = ('Vacation', 'Personal', 'Sick')

class LeaveRequest(db.Model):
    __tablename__ = "leaverequest"

    Rid = db.Column(db.Integer, primary_key=True)  # Unique request ID
    Eid = db.Column(db.Integer, nullable=False)
    Cid = db.Column(db.Integer, nullable=False)
    Sdate = db.Column(db.Date, nullable=False)
    Edate = db.Column(db.Date, nullable=False)
    Type = db.Column(Enum(*LEAVE_TYPES, name="leave_type_enum"), nullable=False)  # maps to leave type
    Status = db.Column(db.String(20), default="Pending", nullable=False)
    ApprovedBy = db.Column(db.Integer, nullable=True)
    CreatedAt = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint(["Eid", "Cid"], ["employee.Eid", "employee.Cid"]),
        db.ForeignKeyConstraint(["ApprovedBy", "Cid"], ["employee.Eid", "employee.Cid"]),
        db.ForeignKeyConstraint(["Cid"], ["company.Cid"]),
        db.ForeignKeyConstraint(["Cid", "Eid", "Type"], ["leave_balance.Cid", "leave_balance.Eid", "leave_balance.LeaveType"]),
    )


# --------------------
# LeaveBalance table (composite PK: Cid + Eid + LeaveType)
# --------------------
class LeaveBalance(db.Model):
    __tablename__ = "leave_balance"

    Cid = db.Column(db.Integer, nullable=False)
    Eid = db.Column(db.Integer, nullable=False)
    LeaveType = db.Column(Enum(*LEAVE_TYPES, name="leave_type_enum"), nullable=False)
    TotalDays = db.Column(db.Integer, nullable=False)
    UsedDays = db.Column(db.Integer, default=0)
    RemainingDays = db.Column(db.Integer, default=0)

    __table_args__ = (
        db.PrimaryKeyConstraint("Cid", "Eid", "LeaveType"),
        # Composite foreign key to ensure the employee exists in the company
        db.ForeignKeyConstraint(["Eid", "Cid"], ["employee.Eid", "employee.Cid"]),
    )


# --------------------
# UserAccount table (composite PK: Cid + Eid)
# --------------------
class UserAccount(db.Model):
    __tablename__ = "user_account"

    Cid = db.Column(db.Integer, nullable=False)
    Eid = db.Column(db.Integer, nullable=False)
    User = db.Column(db.String(50), nullable=False)       # Username
    PassHash = db.Column(db.String(255), nullable=False)  # Hashed password

    __table_args__ = (
        db.PrimaryKeyConstraint("Cid", "Eid"),
        db.ForeignKeyConstraint(["Cid", "Eid"], ["employee.Cid", "employee.Eid"]),
    )
