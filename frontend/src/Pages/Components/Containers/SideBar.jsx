import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { FaBook, FaComments } from "react-icons/fa";

import { ThemeContext } from "../Contexts/ThemeContext";
import { useSideBar } from "../Contexts/SideBarContext";

/**
 * Sidebar component for navigation and layout control.
 * Supports toggling between expanded and collapsed views.
 */
export const Sidebar = () => {
  const { theme } = useContext(ThemeContext);
  const { isExpanded, setIsExpanded } = useSideBar();
  const navigate = useNavigate();

  /** Toggle sidebar between expanded and collapsed */
  const toggleSidebar = () => setIsExpanded(!isExpanded);

  /** Navigate to the Library page */
  const goToLibrary = (e) => {
    e?.preventDefault();
    navigate("/home/library", { replace: true });
  };

  /** Navigate to the Chat page */
  const goToChat = (e) => {
    e?.preventDefault();
    navigate("/home/chat-chatbot", { replace: true });
  };

  /** Image paths for collapse/expand icons depending on theme */
  const collapseIcon =
    theme === "dark"
      ? "/images/sidebar-left-dark-theme.png"
      : "/images/sidebar-left-light-theme.png";

  const expandIcon =
    theme === "dark"
      ? "/images/sidebar-right-dark-theme.png"
      : "/images/sidebar-right-light-theme.png";

  // Common button styles reused across buttons
  const buttonBaseStyle = {
    width: "100%",
    borderRadius: "4px",
    color: "var(--text-color)",
    transition: "all 0.2s ease",
    border: "0",
    padding: "0.5rem 0.5rem",
    backgroundColor: "transparent",
    display: "flex",
    alignItems: "center",
    justifyContent: isExpanded ? "flex-start" : "center",
    cursor: "pointer",
  };

  return (
    <div
      className="d-flex flex-column border-end position-relative"
      style={{
        width: isExpanded ? 200 : 90, // use number for px shorthand
        height: "100vh",
        padding: "20px 0",
        backgroundColor: "var(--bg-sidebar-color)",
        transition: "background 0.3s ease, color 0.3s ease, width 0.3s ease",
        flexShrink: 0, // Prevent shrinking in flex container
      }}
    >
      {/* Container for navigation buttons */}
      <div
        className="d-flex flex-column mt-5 gap-4"
        style={{
          alignItems: isExpanded ? "flex-start" : "center",
          paddingLeft: isExpanded ? 15 : 0,
        }}
      >
        {/* Sidebar toggle button */}
        <button
          onClick={toggleSidebar}
          style={buttonBaseStyle}
          aria-label={isExpanded ? "Collapse sidebar" : "Expand sidebar"}
          title={isExpanded ? "Collapse sidebar" : "Expand sidebar"}
        >
          <img
            src={isExpanded ? collapseIcon : expandIcon}
            alt={isExpanded ? "Collapse sidebar" : "Expand sidebar"}
            style={{ width: 35, height: 35 }}
            draggable={false}
          />
          {isExpanded && (
            <span className="ms-3" style={{ fontSize: "1rem" }}>
              Collapse
            </span>
          )}
        </button>

        {/* Library navigation button */}
        <button onClick={goToLibrary} style={buttonBaseStyle}>
          <FaBook style={{ width: 32, height: 32 }} />
          {isExpanded && (
            <span className="ms-3" style={{ fontSize: "1rem" }}>
              Library
            </span>
          )}
        </button>

        {/* Chat navigation button */}
        <button onClick={goToChat} style={buttonBaseStyle}>
          <FaComments style={{ width: 32, height: 32 }} />
          {isExpanded && (
            <span className="ms-3" style={{ fontSize: "1rem" }}>
              Chat
            </span>
          )}
        </button>
      </div>
    </div>
  );
};