import { Navigate, Outlet } from "react-router-dom";
import { useEffect, useState, useContext } from "react";
import axios from "axios";
import { ThemeContext } from "./Contexts/ThemeContext";
import { useAuth } from "./Contexts/AuthContext";

/**
 * ProtectedRoutes component guards private routes by checking user authentication.
 * It fetches user info on mount, updates global AuthContext and theme accordingly,
 * and controls access to nested routes.
 * 
 * Behavior:
 * - Shows loading indicator while verifying authentication.
 * - Redirects unauthenticated users to "/" (home/login page).
 * - Renders nested routes if authenticated.
 * 
 * @returns {JSX.Element} Loading indicator, redirect, or nested protected routes.
 */
function ProtectedRoutes() {
  // Destructure setters and state from AuthContext
  const { setIsAuthenticated, setSub, setPicture, setName, isAuthenticated } = useAuth();
  // Local loading state to indicate auth status check in progress
  const [loading, setLoading] = useState(true);
  // Access theme toggling from ThemeContext
  const { toggleTheme } = useContext(ThemeContext);

  useEffect(() => {
    // Async function to check authentication by fetching user info
    const checkAuth = async () => {
      try {
        const response = await axios.get("http://localhost:3000/user-info", {
          withCredentials: true, // Send cookies for session auth
        });

        const userData = response.data;

        // Update AuthContext with user info
        if (userData?.sub) setSub(userData.sub.slice(14)); // extract part of sub string
        if (userData?.picture) setPicture(userData.picture);
        if (userData?.name) setName(userData.name);

        // Set theme based on user preference (assumes false means dark)
        const localTheme = localStorage.getItem("theme");
        if (!localTheme) {
          toggleTheme(userData?.userPreference === false ? "dark" : "light");
        }

        setIsAuthenticated(true); // Mark user as authenticated
      } catch (error) {
        // If error occurs (e.g., 401 Unauthorized), mark as not authenticated
        setIsAuthenticated(false);
      } finally {
        // Loading done regardless of success/failure
        setLoading(false);
      }
    };

    checkAuth();
  }, [setIsAuthenticated, setSub, setPicture, setName, toggleTheme]);

  // While loading, show loading indicator
  if (loading) return <div>Loading...</div>;

  // If authenticated, render protected routes; otherwise redirect to home
  return isAuthenticated ? <Outlet /> : <Navigate to="/" />;
}

export default ProtectedRoutes;