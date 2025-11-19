// src/pages/AdminDashboard.js
import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../services/api";
import LOARequestForm from "../components/LOARequestForm";
import CreateEmployeeForm from "../components/CreateEmployeeForm";
import { useNavigate } from "react-router-dom";

function RequestsTable({ requests, showActions = false, onUpdateStatus }) {
  if (!requests || requests.length === 0) {
    return <p>No requests found.</p>;
  }

  return (
    <table
      style={{
        width: "100%",
        borderCollapse: "collapse",
        marginTop: "1rem",
      }}
    >
      <thead>
        <tr>
          <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>
            RID
          </th>
          <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>
            Employee
          </th>
          <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>
            CID
          </th>
          <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>
            Department
          </th>
          <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>
            Start
          </th>
          <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>
            End
          </th>
          <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>
            Type
          </th>
          <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>
            Status
          </th>
          <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>
            Decision By
          </th>
          {showActions && (
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>
              Actions
            </th>
          )}
        </tr>
      </thead>
      <tbody>
        {requests.map((r) => {
          const decisionText = r.approved_by_name
            ? `${r.approved_by_name} (EID ${r.approved_by})`
            : r.approved_by ?? "-";

          return (
            <tr key={r.rid}>
              <td style={{ borderBottom: "1px solid #eee" }}>{r.rid}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>
                {r.employee_name || `${r.eid}`}
              </td>
              <td style={{ borderBottom: "1px solid #eee" }}>{r.cid}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>
                {r.department_name || "-"}
              </td>
              <td style={{ borderBottom: "1px solid #eee" }}>{r.start_date}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>{r.end_date}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>{r.type}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>{r.status}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>{decisionText}</td>
              {showActions && (
                <td style={{ borderBottom: "1px solid #eee" }}>
                  {r.status === "Pending" ? (
                    <>
                      <button
                        onClick={() =>
                          onUpdateStatus(r.rid, "Approved", r.status)
                        }
                        style={{ marginRight: "0.5rem" }}
                      >
                        Approve
                      </button>
                      <button
                        onClick={() =>
                          onUpdateStatus(r.rid, "Rejected", r.status)
                        }
                        style={{ marginRight: "0.5rem" }}
                      >
                        Reject
                      </button>
                    </>
                  ) : (
                    <button
                      onClick={() => onUpdateStatus(r.rid, null, r.status)}
                      style={{ marginRight: "0.5rem" }}
                    >
                      Edit
                    </button>
                  )}
                </td>
              )}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export default function AdminDashboard() {
  const { user, logout } = useAuth(); // user = { cid, eid, username, role, ... }
  const [allRequests, setAllRequests] = useState([]);
  const [activeTab, setActiveTab] = useState("mine"); // "mine" | "others" | "create"
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Filters for "Other Requests"
  const [companyFilter, setCompanyFilter] = useState("ALL");
  const [departmentFilter, setDepartmentFilter] = useState("ALL");

  const navigate = useNavigate();

  async function handleLogout() {
    try {
      await logout();
    } finally {
      navigate("/login");
    }
  }

  async function loadRequests() {
    try {
      setLoading(true);
      setError("");
      const data = await apiFetch("/leave_requests/");
      setAllRequests(data);
    } catch (err) {
      console.error("Failed to load leave requests", err);
      setError("Failed to load leave requests.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadRequests();
  }, []);

  const myRequests = allRequests.filter(
    (r) => r.cid === user?.cid && r.eid === user?.eid
  );
  const otherRequests = allRequests.filter(
    (r) => !(r.cid === user?.cid && r.eid === user?.eid)
  );

  // Unique company + department options based on "otherRequests"
  const companyOptions = Array.from(
    new Set(otherRequests.map((r) => r.cid))
  ).sort((a, b) => (a ?? 0) - (b ?? 0));

  const departmentOptions = Array.from(
    new Set(
      otherRequests
        .map((r) => r.department_name)
        .filter((name) => name && name.trim().length > 0)
    )
  ).sort((a, b) => a.localeCompare(b));

  // Apply filters to otherRequests
  const filteredOtherRequests = otherRequests.filter((r) => {
    const companyMatch =
      companyFilter === "ALL" || r.cid === Number(companyFilter);
    const deptMatch =
      departmentFilter === "ALL" || r.department_name === departmentFilter;
    return companyMatch && deptMatch;
  });

  async function handleUpdateStatus(rid, newStatus, currentStatus) {
    try {
      let statusToSet = newStatus;

      // If newStatus is null, this came from the "Edit" button
      if (!statusToSet) {
        const input = window.prompt(
          "Enter new status (Pending, Approved, Rejected):",
          currentStatus
        );
        if (!input) {
          // cancelled
          return;
        }
        const normalized = input.trim();
        const allowed = ["Pending", "Approved", "Rejected"];
        if (!allowed.includes(normalized)) {
          alert("Invalid status. Please use: Pending, Approved, or Rejected.");
          return;
        }
        if (normalized === currentStatus) {
          // no change
          return;
        }
        statusToSet = normalized;
      }

      await apiFetch(`/leave_requests/${rid}`, {
        method: "PUT",
        body: JSON.stringify({
          status: statusToSet,
          approvedby: user?.eid, // admin’s EID recorded as decision maker
        }),
      });
      await loadRequests();
    } catch (err) {
      console.error("Failed to update status", err);
      alert("Failed to update status. Check console for details.");
    }
  }

  return (
    <div style={{ maxWidth: "1100px", margin: "0 auto", padding: "1.5rem" }}>
      {/* Header with title + logout */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "1rem",
        }}
      >
        <h1>Admin Dashboard</h1>
        <div>
          <span style={{ marginRight: "1rem" }}>
            {user?.username} (CID: {user?.cid}, EID: {user?.eid})
          </span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </div>

      {/* Tabs */}
      <div
        style={{
          marginTop: "1.5rem",
          marginBottom: "1rem",
          display: "flex",
          gap: "0.5rem",
        }}
      >
        <button
          onClick={() => setActiveTab("mine")}
          style={{
            padding: "0.5rem 1rem",
            borderRadius: "4px",
            border:
              activeTab === "mine" ? "2px solid #007bff" : "1px solid #ccc",
            backgroundColor: activeTab === "mine" ? "#007bff" : "#f8f9fa",
            color: activeTab === "mine" ? "#fff" : "#000",
            cursor: "pointer",
          }}
        >
          My Requests
        </button>

        <button
          onClick={() => setActiveTab("others")}
          style={{
            padding: "0.5rem 1rem",
            borderRadius: "4px",
            border:
              activeTab === "others" ? "2px solid #007bff" : "1px solid #ccc",
            backgroundColor: activeTab === "others" ? "#007bff" : "#f8f9fa",
            color: activeTab === "others" ? "#fff" : "#000",
            cursor: "pointer",
          }}
        >
          Other Requests
        </button>

        <button
          onClick={() => setActiveTab("create")}
          style={{
            padding: "0.5rem 1rem",
            borderRadius: "4px",
            border:
              activeTab === "create" ? "2px solid #007bff" : "1px solid #ccc",
            backgroundColor: activeTab === "create" ? "#007bff" : "#f8f9fa",
            color: activeTab === "create" ? "#fff" : "#000",
            cursor: "pointer",
          }}
        >
          Create Employee
        </button>
      </div>

      {loading && activeTab !== "create" && <p>Loading requests...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Tab content */}
      {activeTab === "mine" && !loading && (
        <>
          <h2>Submit New Leave Request</h2>
          <LOARequestForm onSubmitted={loadRequests} />

          <h2 style={{ marginTop: "2rem" }}>My Leave Requests</h2>
          <RequestsTable requests={myRequests} />
        </>
      )}

      {activeTab === "others" && !loading && (
        <>
          <h2>Other Employees&apos; Requests</h2>

          {/* Filters */}
          <div
            style={{
              display: "flex",
              gap: "1rem",
              alignItems: "center",
              marginBottom: "1rem",
              marginTop: "0.5rem",
            }}
          >
            <div>
              <label>
                Company:&nbsp;
                <select
                  value={companyFilter}
                  onChange={(e) => setCompanyFilter(e.target.value)}
                >
                  <option value="ALL">All</option>
                  {companyOptions.map((cid) => (
                    <option key={cid} value={cid}>
                      {cid}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <div>
              <label>
                Department:&nbsp;
                <select
                  value={departmentFilter}
                  onChange={(e) => setDepartmentFilter(e.target.value)}
                >
                  <option value="ALL">All</option>
                  {departmentOptions.map((name) => (
                    <option key={name} value={name}>
                      {name}
                    </option>
                  ))}
                </select>
              </label>
            </div>
          </div>

          <RequestsTable
            requests={filteredOtherRequests}
            showActions={true}
            onUpdateStatus={handleUpdateStatus}
          />
        </>
      )}

      {activeTab === "create" && (
        <div style={{ marginTop: "1rem" }}>
          <CreateEmployeeForm />
        </div>
      )}
    </div>
  );
}
