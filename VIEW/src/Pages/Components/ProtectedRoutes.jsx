import { Navigate, Outlet } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

/**
 * 
 * @returns This Component helps in checking if the user is authenticated, only authenticated users are allowed to enter the protected routes.
 */
function ProtectedRoutes() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  /**
   * In this link the component checks if the user is authenticated, only then will the react component redirect the user to the protected route
   */
  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Call your Flask backend to verify Auth0 session
        const response = await axios.get("http://localhost:3000/api/user", {
            withCredentials: true,
          });
        setIsAuthenticated(true);
      } catch (err) {
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (loading) {
    return <div>Loading...</div>; // Show loader while checking auth
  }

  return isAuthenticated ? <Outlet /> : <Navigate to="/" />;
}

export default ProtectedRoutes;