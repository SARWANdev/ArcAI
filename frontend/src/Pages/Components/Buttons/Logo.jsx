import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { ThemeContext } from "../Contexts/ThemeContext";

export default function Logo({ left = null, right = null }) {
  // Hook to programmatically navigate routes
  const navigate = useNavigate();

  // Get current theme (e.g., "dark" or "light") from ThemeContext
  const { theme } = useContext(ThemeContext);

  // Handler to navigate to the library home page when logo is clicked
  const handleLogoClick = () => {
    navigate("/home/library");
  };

  // Dynamic inline style for the logo positioning and size
  const buttonStyle = {
    width: 115,
    height: 128,
    position: "relative",
    // Conditionally add 'left' or 'right' CSS property as percentage if provided
    ...(left !== null ? { left: `${left}%` } : {}),
    ...(right !== null ? { right: `${right}%` } : {}),
    cursor: "pointer", // Show pointer cursor on hover
  };

  return (
    <img
      // Switch logo image source based on theme
      src={
        theme === "dark"
          ? "/images/b0e06.PNG"
          : "/images/arcai-logo-light-theme.png"
      }
      alt="logo"
      className="img-fluid"
      style={buttonStyle}
      onClick={handleLogoClick}
    />
  );
}
