// src/services/api.js

// We serve React and the API from the same origin (http://localhost:5000),
// so we can use a relative base URL.
const BASE_URL = ""; // same-origin

export async function apiFetch(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: options.method || "GET",
    credentials: "include", // keep using the Flask session cookie
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    body: options.body,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "Request failed");
    console.error("API error", res.status, text);
    throw new Error(text || `HTTP ${res.status}`);
  }

  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return res.json();
  }
  return res.text();
}
