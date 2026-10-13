
import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import { authApi } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("stylehub_token");

    if (!token) {
      setLoading(false);
      return;
    }

    authApi.me()
      .then((response) => setUser(response.data))
      .catch(() => {
        localStorage.removeItem("stylehub_token");
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  async function register(email, password) {
    const response = await authApi.register({ email, password });
    return response.data;
  }

  async function login(email, password) {
    const response = await authApi.login({ email, password });
    const token = response.data.access_token;

    localStorage.setItem("stylehub_token", token);

    try {
      const profile = await authApi.me();
      setUser(profile.data);
    } catch (error) {
      localStorage.removeItem("stylehub_token");
      setUser(null);
      throw error;
    }
  }

  function logout() {
    localStorage.removeItem("stylehub_token");
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{ user, loading, register, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}