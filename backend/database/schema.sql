-- =========================================================
-- 1. Company Table
-- =========================================================
CREATE TABLE company (
    Cid SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    AdminID INT NOT NULL
);

-- =========================================================
-- 2. Department Table
-- =========================================================
CREATE TABLE department (
    Did INT NOT NULL,
    Cid INT NOT NULL,
    Dname VARCHAR(100) NOT NULL,
    ManagerID INT,
    PRIMARY KEY (Did, Cid),
    FOREIGN KEY (Cid) REFERENCES company (Cid)
);

-- =========================================================
-- 3. Employee Table
-- =========================================================
CREATE TABLE employee (
    Eid INT NOT NULL,
    Cid INT NOT NULL,
    Did INT NOT NULL,
    Fname VARCHAR(50) NOT NULL,
    Lname VARCHAR(50) NOT NULL,
    PRIMARY KEY (Eid, Cid),
    FOREIGN KEY (Cid) REFERENCES company (Cid),
    FOREIGN KEY (Did, Cid) REFERENCES department (Did, Cid)
);

-- Add missing FK link for company’s AdminID
ALTER TABLE company
ADD CONSTRAINT fk_admin_employee
FOREIGN KEY (AdminID, Cid) REFERENCES employee (Eid, Cid);

-- =========================================================
-- 4. Leave Balance Table
-- =========================================================
CREATE TYPE leave_type_enum AS ENUM ('Vacation', 'Personal', 'Sick');

CREATE TABLE leave_balance (
    Cid INT NOT NULL,
    Eid INT NOT NULL,
    LeaveType leave_type_enum NOT NULL,
    TotalDays INT NOT NULL,
    UsedDays INT DEFAULT 0,
    RemainingDays INT DEFAULT 0,
    PRIMARY KEY (Cid, Eid, LeaveType),
    FOREIGN KEY (Eid, Cid) REFERENCES employee (Eid, Cid)
);

-- =========================================================
-- 5. Leave Request Table
-- =========================================================
CREATE TABLE leaverequest (
    Rid SERIAL PRIMARY KEY,
    Eid INT NOT NULL,
    Cid INT NOT NULL,
    Sdate DATE NOT NULL,
    Edate DATE NOT NULL,
    Type leave_type_enum NOT NULL,
    Status VARCHAR(20) DEFAULT 'Pending' NOT NULL,
    ApprovedBy INT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (Eid, Cid) REFERENCES employee (Eid, Cid),
    FOREIGN KEY (ApprovedBy, Cid) REFERENCES employee (Eid, Cid),
    FOREIGN KEY (Cid) REFERENCES company (Cid),
    FOREIGN KEY (Cid, Eid, Type) REFERENCES leave_balance (Cid, Eid, LeaveType)
);

-- =========================================================
-- 6. User Account Table
-- =========================================================
CREATE TABLE user_account (
    Cid INT NOT NULL,
    Eid INT NOT NULL,
    User VARCHAR(50) NOT NULL,
    PassHash VARCHAR(255) NOT NULL,
    PRIMARY KEY (Cid, Eid),
    FOREIGN KEY (Cid, Eid) REFERENCES employee (Cid, Eid)
);
