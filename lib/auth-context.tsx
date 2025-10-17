import AsyncStorage from "@react-native-async-storage/async-storage";
import React, { createContext, useContext, useEffect, useState } from "react";

const API_URL = "http://localhost:5000"; // ✅ Flask server base URL

type User = {
  id: number;
  username: string;
};

type AuthContextType = {
  user: User | null;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
  login: (username: string, password: string) => Promise<string | null>;
  signup: (
    username: string,
    email: string,
    password: string
  ) => Promise<string | null>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType>({
  user: null,
  setUser: () => {},
  login: async () => null,
  signup: async () => null,
  logout: async () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  // ✅ Restore user session on app start
  useEffect(() => {
    const loadUser = async () => {
      const storedId = await AsyncStorage.getItem("user_id");
      const storedUsername = await AsyncStorage.getItem("username");
      if (storedId && storedUsername) {
        setUser({ id: Number(storedId), username: storedUsername });
      }
    };
    loadUser();
  }, []);

  // ✅ Signup
  const signup = async (username: string, email: string, password: string) => {
    try {
      const res = await fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await res.json();

      if (!res.ok) return data.error || "Signup failed";

      // Save user session
      await AsyncStorage.setItem("user_id", data.user_id.toString());
      await AsyncStorage.setItem("username", username);
      setUser({ id: data.user_id, username });

      return null; // no error
    } catch (err) {
      console.error("Signup error:", err);
      return "Signup failed due to network error";
    }
  };

  // ✅ Login
  const login = async (username: string, password: string) => {
    try {
      const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (!res.ok) return data.error || "Login failed";

      // Save session
      await AsyncStorage.setItem("user_id", data.user_id.toString());
      await AsyncStorage.setItem("username", username);
      setUser({ id: data.user_id, username });

      return null;
    } catch (err) {
      console.error("Login error:", err);
      return "Login failed due to network error";
    }
  };

  // ✅ Logout
  const logout = async () => {
    await AsyncStorage.removeItem("user_id");
    await AsyncStorage.removeItem("username");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, setUser, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
