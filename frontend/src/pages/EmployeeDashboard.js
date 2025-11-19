// src/pages/EmployeeDashboard.js
import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../services/api";
import LOARequestForm from "../components/LOARequestForm";

export default function EmployeeDashboard() {
  const { user, logout } = useAuth();
  const [requests, setRequests] = useState([]);

  async function loadRequests() {
    if (!user) return;
    const data = await apiFetch(
      `/leave_requests/employee/${user.cid}/${user.eid}`
    );
    setRequests(data);
  }

  useEffect(() => {
    loadRequests();
  }, [user]);

  return (
    <div style={{ padding: "1rem" }}>
      <header style={{ display: "flex", justifyContent: "space-between" }}>
        <h2>Employee Dashboard</h2>
        <button onClick={logout}>Logout</button>
      </header>

      <p>Logged in as: {user?.username}</p>

      <LOARequestForm onCreated={loadRequests} />

      <h3>My Leave Requests</h3>
      <table border="1" cellPadding="4">
        <thead>
          <tr>
            <th>RID</th>
            <th>Type</th>
            <th>Start</th>
            <th>End</th>
            <th>Status</th>
            <th>Approved By</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((r) => (
            <tr key={r.rid}>
              <td>{r.rid}</td>
              <td>{r.type}</td>
              <td>{r.start_date}</td>
              <td>{r.end_date}</td>
              <td>{r.status}</td>
              <td>{r.approved_by || "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
