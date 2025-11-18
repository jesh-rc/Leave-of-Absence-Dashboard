CREATE OR REPLACE VIEW view1 AS
SELECT
    e.eid,
    e.fname,
    e.lname,
    d.did,
    d.dname,
    c.cid,
    c.name AS company_name
FROM employee e
JOIN department d
    ON d.cid = e.cid AND d.did = e.did
JOIN company c
    ON c.cid = e.cid;


CREATE OR REPLACE VIEW view2 AS
SELECT
    d.cid,
    d.did,
    d.dname,
    COUNT(e.eid) AS emp_count
FROM department d
LEFT JOIN employee e
    ON e.cid = d.cid AND e.did = d.did
GROUP BY d.cid, d.did, d.dname
HAVING COUNT(e.eid) >= ALL (
    SELECT COUNT(e2.eid)
    FROM department d2
    LEFT JOIN employee e2
        ON e2.cid = d2.cid AND e2.did = d2.did
    WHERE d2.cid = d.cid
    GROUP BY d2.did
);

CREATE OR REPLACE VIEW view3 AS
SELECT
    e.cid,
    e.eid,
    e.fname,
    e.lname,
    lb.leavetype,
    lb.useddays
FROM employee e
JOIN leave_balance lb
    ON lb.cid = e.cid AND lb.eid = e.eid
WHERE lb.useddays > (
    SELECT AVG(lb2.useddays)
    FROM leave_balance lb2
    WHERE lb2.cid = e.cid
      AND lb2.leavetype = lb.leavetype
);


CREATE OR REPLACE VIEW view4 AS
SELECT
    COALESCE(ua.cid, e.cid) AS cid,
    ua.eid AS account_eid,
    e.eid AS employee_eid,
    ua.username AS username,
    e.fname,
    e.lname
FROM user_account ua
FULL JOIN employee e
    ON ua.cid = e.cid AND ua.eid = e.eid;


CREATE OR REPLACE VIEW view5 AS
WITH needs_action AS (
    SELECT DISTINCT cid, eid
    FROM leaverequest
    WHERE status IN ('Pending', 'Rejected')
),
has_approved AS (
    SELECT DISTINCT cid, eid
    FROM leaverequest
    WHERE status = 'Approved'
)
SELECT e.cid, e.eid, emp.fname, emp.lname
FROM (
    SELECT cid, eid FROM needs_action
    EXCEPT
    SELECT cid, eid FROM has_approved
) e
JOIN employee emp
    ON emp.cid = e.cid AND emp.eid = e.eid;


CREATE OR REPLACE VIEW view6 AS
SELECT
    d.cid,
    d.did,
    d.dname,
    dm.eid AS manager_eid,
    m.fname AS manager_fname,
    m.lname AS manager_lname,
    COUNT(e.eid) AS direct_reports
FROM department d
LEFT JOIN department_manager dm
    ON dm.cid = d.cid AND dm.did = d.did
LEFT JOIN employee m
    ON m.cid = dm.cid AND m.eid = dm.eid
LEFT JOIN employee e
    ON e.cid = d.cid AND e.did = d.did
GROUP BY d.cid, d.did, d.dname, dm.eid, m.fname, m.lname;


CREATE OR REPLACE VIEW view7 AS
SELECT
    lb.cid,
    lb.eid,
    emp.fname,
    emp.lname,
    SUM(lb.totaldays)     AS total_days,
    SUM(lb.useddays)      AS used_days,
    SUM(lb.remainingdays) AS remaining_days
FROM leave_balance lb
JOIN employee emp
    ON emp.cid = lb.cid AND emp.eid = lb.eid
GROUP BY lb.cid, lb.eid, emp.fname, emp.lname;


CREATE OR REPLACE VIEW view8 AS
SELECT
    lr.cid,
    lr.rid,
    lr.eid,
    e.fname,
    e.lname,
    lr.type,
    lr.sdate,
    lr.edate,
    lr.status,
    d.dname
FROM leaverequest lr
JOIN employee e
    ON e.cid = lr.cid AND e.eid = lr.eid
LEFT JOIN department d
    ON d.cid = e.cid AND d.did = e.did
WHERE lr.createdat >= CURRENT_DATE - INTERVAL '30 days';


CREATE OR REPLACE VIEW view9 AS
SELECT
    lr.cid,
    lr.rid,
    lr.eid,
    e.fname,
    e.lname,
    lr.type,
    lr.sdate,
    lr.edate,
    COALESCE(a.fname || ' ' || a.lname, 'Unassigned') AS approver
FROM leaverequest lr
JOIN employee e
    ON e.cid = lr.cid AND e.eid = lr.eid
LEFT JOIN employee a
    ON a.cid = lr.cid AND a.eid = lr.approvedby
WHERE lr.status = 'Pending';


CREATE OR REPLACE VIEW view10 AS
SELECT
    c.cid,
    c.name AS company_name,
    COUNT(DISTINCT e.eid)  AS employees,
    COUNT(DISTINCT ua.eid) AS accounts,
    ROUND(
        100.0 * COUNT(DISTINCT ua.eid) / NULLIF(COUNT(DISTINCT e.eid), 0),
        2
    ) AS pct_with_account
FROM company c
LEFT JOIN employee e
    ON e.cid = c.cid
LEFT JOIN user_account ua
    ON ua.cid = c.cid AND ua.eid = e.eid
GROUP BY c.cid, c.name;

