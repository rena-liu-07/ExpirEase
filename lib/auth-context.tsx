import React, { createContext, ReactNode, useContext, useState } from "react";

// Define what our AuthContext holds
interface AuthContextType {
  user: { id: number; username: string } | null;
  isLoadingUser: boolean;
  signup: (username: string, email: string, password: string) => Promise<string | null>;
  login: (username: string, password: string) => Promise<string | null>;
  logout: () => void;
}

// Create empty context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<AuthContextType["user"]>(null);
  const [isLoadingUser, setIsLoadingUser] = useState(false);

  // 🚀 Signup with Flask API
  const signup = async (username: string, email: string, password: string): Promise<string | null> => {
    setIsLoadingUser(true);
    try {
      const res = await fetch("http://localhost:5000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await res.json() as any;

      if (res.ok) {
        setUser({ id: data.user_id, username });
        return null; // Success, no error
      } else {
        return data.error || "Signup failed";
      }
    } catch (err) {
      console.error("❌ Signup error:", err);
      return "Network error. Please check your connection.";
    } finally {
      setIsLoadingUser(false);
    }
  };

  // 🚀 Login with Flask API
  const login = async (username: string, password: string): Promise<string | null> => {
    setIsLoadingUser(true);
    try {
      const res = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json() as any;

      if (res.ok) {
        setUser({ id: data.user_id, username });
        return null; // Success, no error
      } else {
        return data.error || "Login failed";
      }
    } catch (err) {
      console.error("❌ Login error:", err);
      return "Network error. Please check your connection.";
    } finally {
      setIsLoadingUser(false);
    }
  };

  // 🚀 Logout (clear state + call backend if needed)
  const logout = () => {
    fetch("http://localhost:5000/logout", { method: "POST" }).catch(() => {});
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoadingUser, signup, login, logout }}>
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
