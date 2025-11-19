// src/components/CreateEmployeeForm.js
import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../services/api";

export default function CreateEmployeeForm({ onCreated }) {
  const { user } = useAuth(); // user contains cid, eid, role, etc.

  const [did, setDid] = useState("");
  const [fname, setFname] = useState("");
  const [lname, setLname] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("password123");
  const [status, setStatus] = useState("");

  if (!user || user.role !== "ADMIN") {
    return null;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setStatus("");

    try {
      await apiFetch("/employees/", {
        method: "POST",
        body: JSON.stringify({
          did,
          fname,
          lname,
          email,
          password,
        }),
      });

      setStatus("Employee created successfully.");
      setDid("");
      setFname("");
      setLname("");
      setEmail("");
      setPassword("password123");

      if (onCreated) {
        onCreated();
      }
    } catch (err) {
      console.error("Failed to create employee", err);
      setStatus(
        err?.message || "Failed to create employee. Check console for details."
      );
    }
  }

  return (
    <div
      style={{
        marginBottom: "2rem",
        padding: "1rem",
        border: "1px solid #ddd",
        borderRadius: "4px",
      }}
    >
      <h2>Create New Employee</h2>
      <p style={{ marginTop: 0, fontSize: "0.9rem", color: "#555" }}>
        This will create an employee in your company (CID: {user.cid}) and give
        them a login using the email you enter.
      </p>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "0.5rem" }}>
          <label>
            First Name:&nbsp;
            <input
              type="text"
              value={fname}
              onChange={(e) => setFname(e.target.value)}
              required
            />
          </label>
        </div>

        <div style={{ marginBottom: "0.5rem" }}>
          <label>
            Last Name:&nbsp;
            <input
              type="text"
              value={lname}
              onChange={(e) => setLname(e.target.value)}
              required
            />
          </label>
        </div>

        <div style={{ marginBottom: "0.5rem" }}>
          <label>
            Department ID (DID):&nbsp;
            <input
              type="number"
              value={did}
              onChange={(e) => setDid(e.target.value)}
              required
            />
          </label>
          <div style={{ fontSize: "0.8rem", color: "#777" }}>
            Must match an existing department DID in your company.
          </div>
        </div>

        <div style={{ marginBottom: "0.5rem" }}>
          <label>
            Email (login username):&nbsp;
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>
        </div>

        <div style={{ marginBottom: "0.5rem" }}>
          <label>
            Initial Password:&nbsp;
            <input
              type="text"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
          <div style={{ fontSize: "0.8rem", color: "#777" }}>
            The employee will use this password on first login (they should
            change it later in a real system).
          </div>
        </div>

        <button type="submit">Create Employee</button>

        {status && (
          <p style={{ marginTop: "0.5rem", color: "#006400" }}>{status}</p>
        )}
      </form>
    </div>
  );
}
