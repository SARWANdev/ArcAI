import { Button, Spinner } from "react-bootstrap";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { useAuth } from "../Contexts/AuthContext";
import { useProjects } from "../Contexts/ProjectsContext";
import ProjectRow from "../Containers/ProjectRow";
import "./ProjectGrid.css";

export default function ProjectGrid() {
  // Get user ID from Auth context
  const { sub } = useAuth();

  // Get and set project count from Projects context
  const { projectCount, setProjectCount } = useProjects();

  // State for sorting: which column and order ("asc", "desc", or null)
  const [currentState, setCurrentState] = useState(null);
  const [currentOrder, setCurrentOrder] = useState(null);

  // Projects data and loading state
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  // Currently expanded project index for settings collapse
  const [openIdx, setOpenIdx] = useState(null);

  // Refs to DOM elements for positioning collapse panels and buttons
  const collapseRef = useRef(null);
  const settingsButtonRefs = useRef({});
  const projectRefs = useRef({});
  const projectGridRef = useRef(null);

    // State for the error popup
    const [errorMessage, setErrorMessage] = useState(null);

  // Fetch projects on mount and whenever sorting or projectCount changes
  useEffect(() => {
    getProjects();
  }, [currentState, currentOrder, projectCount]);

  // Fetch projects from backend with optional sorting
  async function getProjects() {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:3000/library/get-projects", {
        params: {
          user_id: sub,
          ...(currentState && currentOrder
            ? { sort_by: currentState, order: currentOrder }
            : {}), // Only add sorting params if sorting is active
        },
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
        },
      });

      const projectList = response.data.data.projects;
      setProjectCount(projectList.length); // Update project count in context
      setProjects(projectList);            // Update projects in state
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to fetch projects.");
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setLoading(false);
    }
  }

  // Toggle sorting order or reset sorting state
  function toggleOrder(column) {
    setLoading(true);

    if (currentState === column) {
      // Cycle through asc -> desc -> no sort
      if (currentOrder === "asc") {
        setCurrentOrder("desc");
      } else if (currentOrder === "desc") {
        setCurrentState(null);
        setCurrentOrder(null);
      } else {
        setCurrentOrder("asc");
      }
    } else {
      // Set new sorting column to ascending order
      setCurrentState(column);
      setCurrentOrder("asc");
    }
  }

  // Close collapse if clicking outside collapse, modal, or settings button
  useEffect(() => {
    function handleClickOutside(event) {
      const clickedInsideCollapse =
        collapseRef.current && collapseRef.current.contains(event.target);
      const clickedInsideModal = event.target.closest(".modal");
      const clickedSettingsButton =
        settingsButtonRefs.current[openIdx] &&
        settingsButtonRefs.current[openIdx].contains(event.target);

      if (!clickedInsideCollapse && !clickedInsideModal && !clickedSettingsButton) {
        setOpenIdx(null);
      }
    }

    if (openIdx !== null) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [openIdx]);

  // Position the collapse panel near the associated project row
  useEffect(() => {
    if (
      openIdx !== null &&
      projectRefs.current[openIdx] &&
      collapseRef.current &&
      projectGridRef.current
    ) {
      const projectEl = projectRefs.current[openIdx];
      const collapseEl = collapseRef.current;
      const containerEl = projectGridRef.current;

      const projectRect = projectEl.getBoundingClientRect();
      const collapseHeight = collapseEl.offsetHeight || 150;

      // Calculate top position below or above the project row
      const topBelow = projectRect.bottom + window.scrollY;
      const topAbove = projectRect.top + window.scrollY - collapseHeight;

      const projectOffsetTop = projectEl.offsetTop;
      const projectHeight = projectEl.offsetHeight;
      const relativeBottom = projectOffsetTop + projectHeight + collapseHeight;
      const containerVisibleBottom = containerEl.scrollTop + containerEl.clientHeight;

      // If collapse would overflow container bottom, position it above instead
      const overflowsBottom = relativeBottom > containerVisibleBottom;
      const top = overflowsBottom ? topAbove : topBelow;

      // Apply absolute positioning to collapse panel
      collapseEl.style.position = "absolute";
      collapseEl.style.top = `${top}px`;
      collapseEl.style.left = `${projectRect.right - 130}px`;
    }
  }, [openIdx]);

  // Render column header label with sorting arrows if active
  function renderSortLabel(label, column) {
    if (currentState === column) {
      if (currentOrder === "asc") return `${label} ▲`;
      if (currentOrder === "desc") return `${label} ▼`;
    }
    return label;
  }

  return (
    <div className="container-fluid px-0">
      {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
      {/* Header row with clickable sortable column labels */}
      <div className="project-header-row mb-4">
        <div
          className={`fw-bold text-truncate ${
            currentState === "Title" ? "text-primary text-decoration-underline" : ""
          }`}
          id="title-button"
          style={{
            flex: 2,
            cursor: "pointer",
            background: "none",
            border: "none",
            padding: 0,
            margin: 0,
            marginLeft: "+6px",
            boxShadow: "none",
          }}
          onClick={() => toggleOrder("Title")}
          tabIndex={0}
        >
          {renderSortLabel("Name", "Title")}
        </div>

        <div
          className={`fw-bold text-truncate ${
            currentState === "CreatedAt" ? "text-primary text-decoration-underline" : ""
          }`}
          id="created-at-button"
          style={{
            flex: 1,
            cursor: "pointer",
            background: "none",
            border: "none",
            padding: 0,
            margin: 0,
            marginLeft: "-75px",
            boxShadow: "none",
          }}
          onClick={() => toggleOrder("CreatedAt")}
          tabIndex={0}
        >
          {renderSortLabel("Created at", "CreatedAt")}
        </div>

        <div
          className={`fw-bold text-truncate ${
            currentState === "LastUpdated" ? "text-primary text-decoration-underline" : ""
          }`}
          id="last-updated-button"
          style={{
            flex: 1,
            cursor: "pointer",
            background: "none",
            border: "none",
            padding: 0,
            margin: 0,
            marginLeft: "-30px",
            boxShadow: "none",
            fontSize: "1.25rem",
          }}
          onClick={() => toggleOrder("LastUpdated")}
          tabIndex={0}
        >
          {renderSortLabel("Updated", "LastUpdated")}
        </div>
      </div>

      {/* Project list or loading / empty state */}
      {loading ? (
        <div className="text-center mt-5">
          <Spinner animation="border" role="status" />
          <div>Loading projects...</div>
        </div>
      ) : projects.length === 0 ? (
        // No projects found message.
        <div
          className="text-center"
          style={{ color: "var(--text-color)" }}
        >
          No projects found.
        </div>
      ) : (

        <div className="overflow-auto" ref={projectGridRef}>
          {projects.map((project, idx) => (
            <ProjectRow
              key={idx}
              index={idx}
              project={project}
              isOpen={openIdx === idx}
              onToggle={() => setOpenIdx(openIdx === idx ? null : idx)}
              onRename={getProjects}
              collapseRef={collapseRef}
              projectRef={(el) => (projectRefs.current[idx] = el)}
              settingsButtonRef={(el) => (settingsButtonRefs.current[idx] = el)}
            />
          ))}
        </div>
      )}
    </div>
  );
}