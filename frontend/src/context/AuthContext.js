// src/context/AuthContext.js
import React, { createContext, useContext, useState } from "react";
import { apiFetch } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  // user = { cid, eid, username, role, ... }

  async function login(email, password) {
    // Backend expects: { username, password }
    const data = await apiFetch("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username: email, password }),
    });

    setUser(data);
    return data;
  }

  async function logout() {
    try {
      await apiFetch("/auth/logout", { method: "POST" });
    } catch (e) {
      // ignore
    }
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
