// src/components/LOARequestForm.js
import React, { useState } from "react";
import { apiFetch } from "../services/api";

const LEAVE_TYPES = [
  { value: "Vacation", label: "Vacation" },
  { value: "Personal", label: "Personal" },
  { value: "Sick", label: "Sick" },
];

export default function LOARequestForm({ onSubmitted }) {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [type, setType] = useState("Vacation"); // default
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");

    try {
      await apiFetch("/leave_requests/", {
        method: "POST",
        body: JSON.stringify({
          sdate: startDate,
          edate: endDate,
          type, // <-- will be "Vacation", "Personal", or "Sick"
        }),
      });

      setStartDate("");
      setEndDate("");
      setType("Vacation");
      if (onSubmitted) onSubmitted();
    } catch (err) {
      console.error("Error submitting LOA:", err);
      setError("Failed to submit request. Please try again.");
    }
  }

  return (
    <form onSubmit={onSubmit}>
      <div>
        <label>
          Start Date
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            required
          />
        </label>
      </div>

      <div>
        <label>
          End Date
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            required
          />
        </label>
      </div>

      <div>
        <label>
          Type
          <select value={type} onChange={(e) => setType(e.target.value)}>
            {LEAVE_TYPES.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
        </label>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <button type="submit">Submit Request</button>
    </form>
  );
}
