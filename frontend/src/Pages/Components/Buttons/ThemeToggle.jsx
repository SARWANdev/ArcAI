import { useContext, useState } from "react";
import { Button } from "react-bootstrap";
import { ThemeContext } from "../Contexts/ThemeContext";
import { useAuth } from "../Contexts/AuthContext";
import axios from "axios";
import "./ThemeToggle.css";

/**
 * ThemeToggle is a button component that allows the user to switch between light and dark themes.
 * It immediately updates the local theme and sends the preference to the backend for persistence.
 */
export default function ThemeToggle() {
  const { theme, toggleTheme } = useContext(ThemeContext); // Access current theme and toggle function from context
  const { sub: user_id } = useAuth(); // Get the authenticated user ID from context
  const [errorMessage, setErrorMessage] = useState(null);

  /**
   * Handles theme toggling:
   * - Toggles the local theme for immediate UI feedback.
   * - Sends the new preference to the backend.
   */
  const handleToggleTheme = async () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    toggleTheme(); // Immediately toggle theme locally

    try {
      // Send the new theme preference to backend
      await axios.post(
        "http://localhost:3000/user/toggle",
        {
          user_id,
          mode: newTheme,
        },
        {
          withCredentials: true,
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log("Theme preference updated successfully.");
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to update preferred mode");
      setTimeout(() => setErrorMessage(null), 5000);
    }
  };

  return (
    <>
    {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
    <Button
      id="theme-toggle-button"
      className="fw-bold wb-1 p-2 mb-2"
      onClick={handleToggleTheme}
      aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
      style={{ transition: "background 0.3s ease, color 0.3s ease" }}
    >
      {/* Button text and emoji based on current theme */}
      {theme === "dark" ? "Light mode ☀️" : "Dark mode 🌙"}
    </Button>
    </>
  );
}
