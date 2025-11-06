-- =========================================================
-- COMPANY
-- =========================================================
INSERT INTO company (Cid, Name, AdminID)
VALUES
(1, 'TechNova Inc', 101),
(2, 'HealthPlus Corp', 201);

-- =========================================================
-- DEPARTMENT
-- =========================================================
INSERT INTO department (Did, Cid, Dname, ManagerID)
VALUES
(1, 1, 'HR', 101),
(2, 1, 'Engineering', 102),
(3, 1, 'Sales', 103),
(1, 2, 'HR', 201),
(2, 2, 'Support', 202),
(3, 2, 'IT', 203);

-- =========================================================
-- EMPLOYEE
-- =========================================================
INSERT INTO employee (Eid, Cid, Did, Fname, Lname)
VALUES
(101, 1, 1, 'Alice', 'Johnson'),   -- Manager HR
(104, 1, 1, 'Iris', 'Chen'),       -- Extra HR employee
(102, 1, 2, 'Bob', 'Lee'),         -- Manager Engineering
(105, 1, 2, 'Jack', 'Smith'),      -- Extra Engineering
(103, 1, 3, 'Clara', 'Wong'),      -- Manager Sales
(106, 1, 3, 'Liam', 'Davis'),      -- Extra Sales
(201, 2, 1, 'David', 'Nguyen'),    -- Manager HR
(204, 2, 1, 'Mona', 'Patel'),      -- Extra HR
(202, 2, 2, 'Ella', 'Brown'),      -- Manager Support
(205, 2, 2, 'Nate', 'Kim'),        -- Extra Support
(203, 2, 3, 'Frank', 'Miller'),    -- Manager IT
(206, 2, 3, 'Olivia', 'Lopez');    -- Extra IT

-- =========================================================
-- LEAVE BALANCE
-- =========================================================
INSERT INTO leave_balance (Cid, Eid, LeaveType, TotalDays, UsedDays, RemainingDays)
VALUES
(1, 101, 'Vacation', 15, 10, 5),
(1, 104, 'Vacation', 15, 5, 10),
(1, 102, 'Sick', 10, 6, 4),
(1, 105, 'Sick', 10, 3, 7),
(1, 103, 'Personal', 5, 3, 2),
(1, 106, 'Personal', 5, 1, 4),
(2, 201, 'Vacation', 15, 8, 7),
(2, 204, 'Vacation', 15, 4, 11),
(2, 202, 'Sick', 10, 2, 8),
(2, 205, 'Sick', 10, 0, 10),
(2, 203, 'Personal', 5, 2, 3),
(2, 206, 'Personal', 5, 1, 4);

-- =========================================================
-- LEAVE REQUESTS
-- =========================================================
INSERT INTO leaverequest (Eid, Cid, Sdate, Edate, Type, Status, ApprovedBy, CreatedAt)
VALUES
(101, 1, '2025-09-01', '2025-09-05', 'Vacation', 'Approved', 102, CURRENT_DATE - 40),
(102, 1, '2025-10-10', '2025-10-12', 'Sick', 'Pending', NULL, CURRENT_DATE - 5),
(103, 1, '2025-07-15', '2025-07-16', 'Personal', 'Approved', 101, CURRENT_DATE - 20),
(104, 1, '2025-10-01', '2025-10-02', 'Vacation', 'Pending', NULL, CURRENT_DATE - 2),
(105, 1, '2025-09-20', '2025-09-22', 'Sick', 'Rejected', 102, CURRENT_DATE - 10),
(106, 1, '2025-09-25', '2025-09-27', 'Personal', 'Approved', 103, CURRENT_DATE - 15),
(201, 2, '2025-08-01', '2025-08-10', 'Vacation', 'Approved', 203, CURRENT_DATE - 35),
(202, 2, '2025-09-15', '2025-09-17', 'Sick', 'Pending', NULL, CURRENT_DATE - 3),
(203, 2, '2025-10-01', '2025-10-02', 'Personal', 'Rejected', 201, CURRENT_DATE - 7),
(204, 2, '2025-09-28', '2025-09-30', 'Vacation', 'Pending', NULL, CURRENT_DATE - 4),
(205, 2, '2025-09-22', '2025-09-24', 'Sick', 'Approved', 202, CURRENT_DATE - 12),
(206, 2, '2025-10-02', '2025-10-03', 'Personal', 'Approved', 203, CURRENT_DATE - 1);

-- =========================================================
-- USER ACCOUNT
-- =========================================================
INSERT INTO user_account (Cid, Eid, User, PassHash)
VALUES
(1, 101, 'alicej', 'hash123'),
(1, 102, 'boblee', 'hash234'),
(1, 103, 'claraw', 'hash345'),
(1, 104, 'irisc', 'hash890'),
(1, 105, 'jacks', 'hash901'),
(1, 106, 'liamd', 'hash902'),
(2, 201, 'davidn', 'hash456'),
(2, 202, 'ellab', 'hash567'),
(2, 203, 'frankm', 'hash678'),
(2, 204, 'monap', 'hash789'),
(2, 205, 'natek', 'hash890'),
(2, 206, 'olivial', 'hash891');
