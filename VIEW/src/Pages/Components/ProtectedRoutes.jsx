import { Navigate, Outlet } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "./AuthContext"; // import your context

function ProtectedRoutes() {
  const { setIsAuthenticated, setUser, isAuthenticated } = useAuth();  // use context
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await axios.get("http://localhost:3000/api/user", {
          withCredentials: true,
        });

        const userinfo = response.data?.userinfo;
        setUser(userinfo);               // store user info (e.g., picture)
        setIsAuthenticated(true);        // mark as authenticated
      } catch (err) {
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return <>{isAuthenticated ? <Outlet /> : <Navigate to="/" />}</>;
}

export default ProtectedRoutes;