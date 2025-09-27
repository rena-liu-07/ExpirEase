import { createContext, useContext, useState } from "react";

type AuthContextType = {
  user: { user_id: number; username: string } | null;
  isLoadingUser: boolean;
  signUp: (
    username: string,
    email: string,
    password: string
  ) => Promise<string | null>;
  signIn: (username: string, password: string) => Promise<string | null>;
  signOut: () => Promise<void>;
};
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<{
    user_id: number;
    username: string;
  } | null>(null);
  const [isLoadingUser, setIsLoadingUser] = useState<boolean>(false);

  // Optionally: useEffect to check for persisted login

  const signUp = async (username: string, email: string, password: string) => {
    try {
      const res = await fetch("http://localhost:5000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });
      const data = await res.json();
      if (res.ok && data.user_id) {
        setUser({ user_id: data.user_id, username });
        return null;
      } else {
        return data.error || "Signup failed";
      }
    } catch (error) {
      return "Network error";
    }
  };

  const signIn = async (username: string, password: string) => {
    try {
      const res = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (res.ok && data.user_id) {
        setUser({ user_id: data.user_id, username });
        return null;
      } else {
        return data.error || "Login failed";
      }
    } catch (error) {
      return "Network error";
    }
  };

  const signOut = async () => {
    setUser(null);
    // Optionally: clear async storage
  };

  return (
    <AuthContext.Provider
      value={{ user, isLoadingUser, signUp, signIn, signOut }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be inside of the AuthProvider");
  }
  return context;
}
