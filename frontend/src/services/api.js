// src/services/api.js

// We rely on CRA's proxy, so we do NOT hard-code http://localhost:5000 here.
// The browser will call relative URLs like "/auth/login", which are same-origin
// for http://localhost:3000. The dev server then proxies to Flask.

export async function apiFetch(path, options = {}) {
  const url = path; // e.g. "/auth/login"

  console.log("API request to:", url); // debug

  const response = await fetch(url, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let errorBody;
    try {
      errorBody = await response.json();
    } catch {
      const text = await response.text();
      const err = new Error(`HTTP ${response.status}`);
      err.status = response.status;
      err.raw = text;
      throw err;
    }

    const err = new Error(errorBody.message || `HTTP ${response.status}`);
    Object.assign(err, errorBody, { status: response.status });
    throw err;
  }

  if (response.status === 204) return null;

  return response.json();
}
