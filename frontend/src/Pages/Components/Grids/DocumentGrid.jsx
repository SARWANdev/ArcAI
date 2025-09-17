import { Spinner } from "react-bootstrap";
import { useState, useEffect, useRef, useContext } from "react";
import axios from "axios";
import { useAuth } from "../Contexts/AuthContext";
import { useProjects } from "../Contexts/ProjectsContext";
import { FilterContext } from "../../ProjectViewerPage";
import { useSideBar } from "../Contexts/SideBarContext";
import DocumentRow from "../Containers/DocumentRow";
import "./DocumentGrid.css";

// Display labels for the document header fields
const displayLabels = {
  Title: "Name",
  Author: "Author",
  Year: "Year",
  Source: "Source",
  AddedAt: "Added at",
};

export default function DocumentGrid({ project_id, refreshFlag }) {
  // Global filter state from context
  const { filterState } = useContext(FilterContext);
  // Document count and setter from ProjectsContext
  const { documentCount, setDocumentCount } = useProjects();
  // Current user id (sub) from AuthContext
  const { sub } = useAuth();

  // Sort state: { field: string, order: 'asc' | 'desc' } or null (no sort)
  const [sortState, setSortState] = useState(null);
  // List of document objects fetched from backend
  const [documents, setDocuments] = useState([]);
  // Sets of document IDs marked as favorite or read
  const [favourite, setFavourite] = useState(new Set());
  const [read, setRead] = useState(new Set());
  // Loading indicator while fetching documents
  const [loading, setLoading] = useState(true);
  // Currently open settings menu index
  const [openIdx, setOpenIdx] = useState(null);

  // Refs to settings buttons for detecting outside clicks
  const settingsButtonRefs = useRef({});
  // Sidebar expansion state
  const { isExpanded } = useSideBar();
  // Ref to the open settings collapse element for positioning
  const collapseRef = useRef(null);

    // State for the error popup
    const [errorMessage, setErrorMessage] = useState(null);

  // Helper: normalize header field to backend field name
  function normalizeField(field) {
    return field === "AddedAt" ? "created_at" : field.toLowerCase();
  }

  // Handle toggling sorting states on header clicks
  function toggleSort(field) {
    const normalized = normalizeField(field);
    if (!sortState || sortState.field !== normalized) {
      setSortState({ field: normalized, order: "asc" });
    } else if (sortState.order === "asc") {
      setSortState({ field: normalized, order: "desc" });
    } else {
      setSortState(null); // Clear sort
    }
  }

  // Format date string as days ago (e.g. "3 days ago", "Today")
  function formatDaysAgo(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    const diffMs = new Date() - date;
    const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    if (days < 1) return "Today";
    return `${days} day${days !== 1 ? 's' : ''} ago`;
  }

  // Fetch documents when sort, filter, documentCount, or refreshFlag change
  useEffect(() => {
    getDocumentsFromProjectId();
  }, [sortState, filterState, documentCount, refreshFlag]);

  // Detect clicks outside open settings menu to close it
  useEffect(() => {
    function handleClickOutside(event) {
      const clickedOutside =
        !collapseRef.current?.contains(event.target) &&
        !settingsButtonRefs.current[openIdx]?.contains(event.target) &&
        !event.target.closest(".modal");
      if (clickedOutside) setOpenIdx(null);
    }

    if (openIdx !== null) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [openIdx]);

  // Position the settings menu relative to the corresponding row and container
  useEffect(() => {
    if (
      openIdx !== null &&
      settingsButtonRefs.current[openIdx] &&
      collapseRef.current &&
      document.querySelector('.document-scroll-container')
    ) {
      const rowEl = settingsButtonRefs.current[openIdx].closest('.col-md-12');
      const collapseEl = collapseRef.current;
      const containerEl = document.querySelector('.document-scroll-container');

      const relativeTop = rowEl.offsetTop;
      const collapseHeight = collapseEl.offsetHeight || 150;

      const topBelow = relativeTop + rowEl.offsetHeight;
      const topAbove = relativeTop - collapseHeight;

      // Check if menu would overflow container bottom
      const overflowsBottom = (relativeTop + rowEl.offsetHeight + collapseHeight) > (containerEl.scrollTop + containerEl.clientHeight);
      const top = overflowsBottom ? topAbove : topBelow;

      // Position absolutely relative to scroll container
      collapseEl.style.position = "absolute";
      collapseEl.style.top = `${top}px`;
      collapseEl.style.left = `${rowEl.offsetLeft + rowEl.offsetWidth - 150}px`;
    }
  }, [openIdx]);

  // Fetch documents from backend API for given project and current filters/sorts
  async function getDocumentsFromProjectId() {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:3000/project/get-documents", {
        params: {
          user_id: sub,
          project_id,
          sort_states: sortState ? JSON.stringify([sortState]) : "[]",
          filter_state: filterState?.type || filterState,
          tagname: filterState?.type === "ByTag" ? filterState.tag : undefined,
        },
        withCredentials: true,
        headers: { "Content-Type": "application/json" },
      });

      const docs = response.data.documents;

      setDocuments(docs);
      setDocumentCount(docs.length);

      // Update favorite and read sets for quick lookup
      setFavourite(new Set(docs.filter(doc => doc.Favorite).map(doc => doc.DocumentId)));
      setRead(new Set(docs.filter(doc => doc.Read).map(doc => doc.DocumentId)));

      setLoading(false);
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to fetch documents.");
      setTimeout(() => setErrorMessage(null), 5000);
      setLoading(false);
    }
  }

  return (
    <div className="container-fluid px-0">
      {/* The error popup element */}
      {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
      {/* Document header row with clickable sortable columns */}
      <div className="document-header-row mb-4">
        {/* Title column */}
        <div
          className={`fw-bold text-truncate ${sortState?.field === "title" ? "text-primary text-decoration-underline" : ""}`}
          id="document-title-button"
          style={{ flex: 2, cursor: "pointer", background: "none", border: "none", padding: 0, margin: 0, marginLeft: "52px", boxShadow: "none" }}
          onClick={() => toggleSort("Title")}
          tabIndex={0}
        >
          Name {sortState?.field === "title" ? (sortState.order === "asc" ? "▲" : "▼") : ""}
        </div>

        {/* Author column */}
        <div
          className={`fw-bold text-truncate ${sortState?.field === "author" ? "text-primary text-decoration-underline" : ""}`}
          id="author-button"
          style={{ flex: 1, cursor: "pointer", background: "none", border: "none", padding: 0, margin: 0, marginLeft: "-70px", boxShadow: "none" }}
          onClick={() => toggleSort("Author")}
          tabIndex={0}
        >
          Author {sortState?.field === "author" ? (sortState.order === "asc" ? "▲" : "▼") : ""}
        </div>

        {/* Year column */}
        <div
          className={`fw-bold text-truncate ${sortState?.field === "year" ? "text-primary text-decoration-underline" : ""}`}
          id="year-button"
          style={{ flex: 1, cursor: "pointer", background: "none", border: "none", padding: 0, margin: 0, marginLeft: "-30px", boxShadow: "none" }}
          onClick={() => toggleSort("Year")}
          tabIndex={0}
        >
          Year {sortState?.field === "year" ? (sortState.order === "asc" ? "▲" : "▼") : ""}
        </div>

        {/* Source column */}
        <div
          className={`fw-bold text-truncate ${sortState?.field === "source" ? "text-primary text-decoration-underline" : ""}`}
          id="source-button"
          style={{ flex: 2, cursor: "pointer", background: "none", border: "none", padding: 0, margin: 0, marginLeft: "-46px", boxShadow: "none" }}
          onClick={() => toggleSort("Source")}
          tabIndex={0}
        >
          Source {sortState?.field === "source" ? (sortState.order === "asc" ? "▲" : "▼") : ""}
        </div>

        {/* AddedAt column */}
        <div
          className={`fw-bold text-truncate ${sortState?.field === "created_at" ? "text-primary text-decoration-underline" : ""}`}
          id="addedat-button"
          style={{ flex: 1, cursor: "pointer", background: "none", border: "none", padding: 0, margin: 0, marginLeft: "-72px", boxShadow: "none" }}
          onClick={() => toggleSort("AddedAt")}
          tabIndex={0}
        >
          Added at {sortState?.field === "created_at" ? (sortState.order === "asc" ? "▲" : "▼") : ""}
        </div>
      </div>

      {/* Loading indicator */}
      {loading ? (
        <div className="text-center mt-5">
          <Spinner animation="border" role="status" />
          <div>Loading documents...</div>
        </div>
      ) : documents.length === 0 ? (
        // No documents found message.
        <div
          className="text-center"
          style={{ color: "var(--text-color)" }}
        >
          No documents found.
        </div>
      ) : (
        // Scrollable container for document rows
        <div className="document-scroll-container overflow-auto">
          {documents.map((doc, idx) => (
            <DocumentRow
              key={doc.DocumentId}
              document={doc}
              idx={idx}
              favourite={favourite}
              setFavourite={setFavourite}
              read={read}
              setRead={setRead}
              project_id={project_id}
              sub={sub}
              openIdx={openIdx}
              setOpenIdx={setOpenIdx}
              settingsButtonRefs={settingsButtonRefs}
              collapseRef={collapseRef}
              isExpanded={isExpanded}
              refreshDocuments={getDocumentsFromProjectId}
              formatDaysAgo={formatDaysAgo}
            />
          ))}
        </div>
      )}
    </div>
  );
}