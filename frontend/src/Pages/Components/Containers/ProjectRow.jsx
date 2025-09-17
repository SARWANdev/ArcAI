import { useEffect } from "react";
import DeleteButton from "../Buttons/DeleteButton";
import DownloadButton from "../Buttons/DownloadButton";
import UploadButton from "../Buttons/UploadButton";
import RenameButton from "../Buttons/RenameButton";
import { useSideBar } from "../Contexts/SideBarContext";

/**
 * Component representing a single project row in a list.
 * Shows project title, creation and update times, and a settings toggle.
 * Supports collapsing an inline settings panel with project actions.
 *
 * @param {Object} props
 * @param {Object} props.project - Project data object.
 * @param {number} props.index - Index of this project row.
 * @param {boolean} props.isOpen - Whether the settings panel is open.
 * @param {Function} props.onToggle - Function to toggle the settings panel.
 * @param {Function} props.onRename - Callback for rename action.
 * @param {React.RefObject} props.collapseRef - Ref for the collapsible settings element.
 * @param {React.RefObject} props.projectRef - Ref for the project row element.
 * @param {React.RefObject} props.settingsButtonRef - Ref for the settings button element.
 */
export default function ProjectRow({
  project,
  index,
  isOpen,
  onToggle,
  onRename,
  collapseRef,
  projectRef,
  settingsButtonRef,
}) {
  const { isExpanded } = useSideBar();

  /**
   * Helper to format a date string into a relative "time ago" string.
   *
   * @param {string} dateString - ISO date string.
   * @returns {string} Formatted relative time ago string.
   */
  function formatDaysAgo(dateString) {
    if (!dateString) return "";
    const utcDate = new Date(dateString);
    const now = new Date();
    const diffMs = now - utcDate;

    const seconds = Math.floor(diffMs / 1000);
    const minutes = Math.floor(diffMs / (1000 * 60));
    const hours = Math.floor(diffMs / (1000 * 60 * 60));
    const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (seconds < 60) return `${seconds} second${seconds !== 1 ? "s" : ""} ago`;
    if (minutes < 60) return `${minutes} minute${minutes !== 1 ? "s" : ""} ago`;
    if (hours < 24) return `${hours} hour${hours !== 1 ? "s" : ""} ago`;
    return `${days} day${days !== 1 ? "s" : ""} ago`;
  }

  /**
   * Handle clicking on the project row.
   * Navigates to the project detail page unless clicking on settings or card body.
   *
   * @param {MouseEvent} e
   */
  const handleRowClick = (e) => {
    // Prevent navigation if clicking settings button or card body inside the row
    if (e.target.closest(".settings-button") || e.target.closest(".card-body")) {
      return;
    }
    // Redirect to project details page
    window.location.href = `http://localhost:5173/home/library/project/${project.ProjectId}/${project.Title}`;
  };

  /**
   * Adjusts the position of the collapsible settings panel so it stays
   * visible within the scrolling container.
   */
  useEffect(() => {
    if (!isOpen || !projectRef.current || !collapseRef.current) return;

    const projectEl = projectRef.current;
    const collapseEl = collapseRef.current;
    const containerEl = document.querySelector(".overflow-auto");

    const projectRect = projectEl.getBoundingClientRect();
    const collapseHeight = collapseEl.offsetHeight || 150;

    const topBelow = projectRect.bottom + window.scrollY; // Position below project row
    const topAbove = projectRect.top + window.scrollY - collapseHeight; // Position above project row

    const projectOffsetTop = projectEl.offsetTop;
    const projectHeight = projectEl.offsetHeight;
    const relativeBottom = projectOffsetTop + projectHeight + collapseHeight;
    const containerVisibleBottom = containerEl.scrollTop + containerEl.clientHeight;

    // If panel would overflow container bottom, show above instead of below
    const overflowsBottom = relativeBottom > containerVisibleBottom;
    const top = overflowsBottom ? topAbove : topBelow;

    // Apply absolute positioning to collapse panel
    collapseEl.style.position = "absolute";
    collapseEl.style.top = `${top}px`;
    collapseEl.style.left = `${projectRect.right - 130}px`;
  }, [isOpen, projectRef, collapseRef]);

  return (
    <div className="col-md-12" ref={projectRef}>
      {/* Entire row clickable */}
      <div
        className="project-row p-2"
        id="project-button"
        style={{ height: "80px", cursor: "pointer" }}
        onClick={handleRowClick}
      >
        {/* Project Title */}
        <div className="text-truncate" id="project-title">
          {project.Title}
        </div>
        {/* Created At relative time */}
        <div className="text-truncate" id="project-created-at">
          {formatDaysAgo(project.CreatedAt)}
        </div>
        {/* Last Updated relative time */}
        <div className="text-truncate" id="project-last-updated">
          {formatDaysAgo(project.LastUpdated)}
        </div>
        {/* Settings Button: clicking toggles settings panel */}
        <button
          ref={settingsButtonRef}
          className="btn btn-sm btn-outline-secondary settings-button"
          type="button"
          onClick={(e) => {
            e.stopPropagation(); // Prevent row click handler
            onToggle();
          }}
        />
      </div>

      {/* Collapsible Settings Panel */}
      {isOpen && (
        <div
          ref={collapseRef}
          id={`settings-${index}`}
          style={{
            width: "130px",
            position: "absolute",
            left: isExpanded ? "90%" : "85.5%",
            zIndex: 1000,
          }}
        >
          <div className="card card-body mt-2 p-2" style={{ backgroundColor: "var(--bg-color)" }}>
            <DeleteButton project_id={project.ProjectId} onCloseSettings={onToggle} />
            <DownloadButton project_id={project.ProjectId} />
            <UploadButton project_id={project.ProjectId} />
            <RenameButton
              project_id={project.ProjectId}
              project_title={project.Title}
              onRename={onRename}
            />
          </div>
        </div>
      )}
    </div>
  );
}