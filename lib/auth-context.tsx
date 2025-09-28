import React, { createContext, ReactNode, useContext, useState } from "react";

// Define what our AuthContext holds
interface AuthContextType {
  user: { id: number; username: string } | null;
  signup: (username: string, email: string, password: string) => Promise<void>;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

// Create empty context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<AuthContextType["user"]>(null);

  // 🚀 Signup with Flask API
  const signup = async (username: string, email: string, password: string) => {
    try {
      const res = await fetch("http://localhost:8080/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await res.json() as any;

      if (res.ok) {
        setUser({ id: data.user_id, username });
      } else {
        throw new Error(data.error || "Signup failed");
      }
    } catch (err) {
      console.error("❌ Signup error:", err);
    }
  };

  // 🚀 Login with Flask API
  const login = async (username: string, password: string) => {
    try {
      const res = await fetch("http://localhost:8080/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json() as any;

      if (res.ok) {
        setUser({ id: data.user_id, username });
      } else {
        throw new Error(data.error || "Login failed");
      }
    } catch (err) {
      console.error("❌ Login error:", err);
    }
  };

  // 🚀 Logout (clear state + call backend if needed)
  const logout = () => {
    fetch("http://localhost:8080/logout", { method: "POST" }).catch(() => {});
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, signup, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook to use AuthContext easily
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside an AuthProvider");
  }
  return context;
};
