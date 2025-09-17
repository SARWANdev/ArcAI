import { createContext, useState } from "react";
import { useParams } from "react-router-dom";
import DocumentGrid from "./Components/Grids/DocumentGrid";
import FilterButton from "./Components/Buttons/FilterButton";
import UploadButton from "./Components/Buttons/UploadButton";
import NoteButton from "./Components/Buttons/NoteButton";
import PageLayout from "./Components/Containers/PageLayout";
import SearchBar from "./Components/Buttons/SearchBar";

// Create a context to share filter state between components in this page
export const FilterContext = createContext();

export default function ProjectViewerPage() {
  // Extract URL parameters (e.g. projectId, title) via react-router hook
  const params = useParams();

  // Local state to hold current filter settings (can be null initially)
  const [filterState, setFilterState] = useState(null);

  // State flag to trigger refresh of DocumentGrid when documents change (upload etc)
  const [refreshDocumentsFlag, setRefreshDocumentsFlag] = useState(false);

  // Callback to be called after successful upload - toggles refresh flag to cause document reload
  function handleUploadComplete() {
    setRefreshDocumentsFlag(prev => !prev);
  }

  return (
    // Provide filterState and its setter to all child components via context
    <FilterContext.Provider value={{ filterState, setFilterState }}>
      <PageLayout>
        {/* Page title from URL param */}
        <h1 className="fs-1 fw-bold mb-4">{params.title}</h1>

        {/* Container for controls: search bar, upload button, note button, filter button */}
        <div className="row g-2 align-items-center mb-4">
          <div className="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
            <div className="d-flex justify-content-between">
              {/* Search input component, passed prop ifDoc=true for document context */}
              <SearchBar ifDoc={true} />

              {/* Upload button tied to the current project; triggers refresh on completion */}
              <UploadButton
                project_id={params.projectId}
                onUploadComplete={handleUploadComplete}
              />

              {/* Note button for project-level notes */}
              <NoteButton project_id={params.projectId} />

              {/* Filter button to apply filters for this project */}
              <FilterButton project_id={params.projectId} />
            </div>
          </div>
        </div>

        {/* Document grid shows documents for the current project, refreshes on flag toggle */}
        <DocumentGrid
          project_id={params.projectId}
          refreshFlag={refreshDocumentsFlag}
        />
      </PageLayout>
    </FilterContext.Provider>
  );
}