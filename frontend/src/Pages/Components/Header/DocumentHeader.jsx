import { Button } from "react-bootstrap";

export default function DocumentHeader({ sortState, toggleSort }) {
  // Mapping of field keys to display labels
  const displayLabels = {
    Title: "Title",
    Author: "Author",
    Year: "Year",
    Source: "Source",
    AddedAt: "Added at",
  };

  // List of sortable fields in order
  const fields = ["Title", "Author", "Year", "Source", "AddedAt"];

  // Map fields to button IDs for accessibility/testing
  const idMap = {
    Title: "document-title-button",
    Author: "author-button",
    Year: "year-button",
    Source: "source-button",
    AddedAt: "addedat-button",
  };

  return (
    <div className="container-fluid d-flex row mb-4">
      {fields.map((field) => {
        // Determine if this field is currently active in the sort state
        // Note: "AddedAt" corresponds to sortState.field === "created_at"
        const isActive = sortState?.field === (field === "AddedAt" ? "created_at" : field.toLowerCase());

        // Show ascending or descending arrow based on current sort order
        const arrow = isActive ? (sortState.order === "asc" ? "▲" : "▼") : "";

        return (
          <Button
            key={field}
            id={idMap[field]}
            onClick={() => toggleSort(field)}
            className={`btn border-0 ${isActive ? "fw-bold text-decoration-underline text-primary" : ""}`}
            style={{ backgroundColor: "var(--bg-button-color)", color: "var(--bg-text-color)" }}
            title={displayLabels[field]} // Tooltip for accessibility
          >
            {displayLabels[field]} {arrow}
          </Button>
        );
      })}
    </div>
  );
}