import { Button, Modal } from "react-bootstrap";
import { useState, useEffect, useRef, useContext } from "react";
import { useSideBar } from "../Contexts/SideBarContext";
import { FilterContext } from "../../ProjectViewerPage";
import axios from "axios";
import { useAuth } from "../Contexts/AuthContext";
import "./FilterButton.css";

export default function FilterButton({project_id}) {
  const [toOpen, setToOpen] = useState(false);
  const [showTagModal, setShowTagModal] = useState(false); // ← NEW
  const { isExpanded } = useSideBar();
  const filterRef = useRef(null);
  const filterButtonRef = useRef(null);
  const { sub } = useAuth(); // Get user ID
  const [tagList, setTagList] = useState({});
  const [selectedTag, setSelectedTag] = useState(null);
  const { filterState, setFilterState } = useContext(FilterContext);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (
        filterRef.current &&
        !filterRef.current.contains(event.target) &&
        filterButtonRef.current &&
        !filterButtonRef.current.contains(event.target)
      ) {
        setToOpen(false);
      }
    }

    if (toOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [toOpen]);

  useEffect(() => {
    if (showTagModal) {
      fetchTagsfromProject();
      if (filterState?.type === "ByTag") {
        setSelectedTag(filterState.tag);
      } else {
        setSelectedTag(null);
      }
    }
  }, [showTagModal]);

  async function fetchTagsfromProject() {
    try {
      const response = await axios.get("http://localhost:3000/project/tags", {
        params: {
          user_id : sub,
          project_id,
        },
        withCredentials: true,
      });
  
      const tags = response.data.tags || []; // Adjust based on your backend response
      setTagList(tags);
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Error getting tags from the backend.");
      setTimeout(() => setErrorMessage(null), 5000);
    }
  }

  function toggleTagSelection(tag) {
    setSelectedTag(tag === selectedTag ? null : tag);
  }

  return (
    <>
      {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
      {/* Filter Button */}
      <Button
        ref={filterButtonRef}
        title="filter"
        id="filter-button"
        onClick={() => setToOpen((prev) => !prev)}
      >
        Filter
      </Button>

      {/* Dropdown */}
      <div
        ref={filterRef}
        className="filter-collapsable container-fluid flex-column justify-content-center"
        id="filter-collapsable"
        style={{
          width: "170px",
          height: "150px",
          backgroundColor: "var(--bg-button-color)",
          display: toOpen ? "flex" : "none",
          position: "absolute",
          left: isExpanded ? "89vw" : "84vw",
          bottom: "51vh",
          transition: "background 0.3s ease, color 0.3s ease",
          border: "1px solid #d4d4d4",
          borderRadius: "5px",
          zIndex: "1000"
        }}
      >
        <Button
          className={`mb-2 fw-bold ${
            filterState === "ByFavourite" ? "text-decoration-underline text-primary" : ""
          }`}
          id="by-favourites-button"
          onClick={() => {
            setFilterState(filterState === "ByFavourite" ? null : "ByFavourite");
          }}
        >
          {filterState === "ByFavourite" ? "By Favourites ✓" : "By Favourites"}
        </Button>

        <Button
          id="by-tags-button"
          className="mb-2 fw-bold"
          onClick={() => setShowTagModal(true)}
        >
          {filterState?.type === "ByTag" ? "By Tags ✓" : "By Tags"}
        </Button>

        <Button
          className={`mb-2 fw-bold ${
            filterState === "IfRead" ? "text-decoration-underline text-primary" : ""
          }`}
          id="if-read-button"
          onClick={() => {
            setFilterState(filterState === "IfRead" ? null : "IfRead");
          }}
        >
          {filterState === "IfRead" ? "If Read ✓" : "If Read"}
        </Button>
      </div>

      {/* Modal for Filter by Tags */}
      <Modal
        show={showTagModal}
        onHide={() => setShowTagModal(false)}
        centered
        size="md"
      >
        <Modal.Header closeButton>
          <Modal.Title>Filter by Tags</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {Object.keys(tagList).length > 0 ? (
            <ul className="list-unstyled">
              {Object.entries(tagList).map(([tag, color], idx) => (
                <li
                  key={idx}
                  onClick={() => toggleTagSelection(tag)}
                  style={{
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    padding: "6px 0",
                    fontWeight: selectedTag === tag ? "bold" : "normal",
                    color
                  }}
                >
                  <span style={{ width: "20px", textAlign: "center" }}>
                    {selectedTag === tag ? "✓" : ""}
                  </span>
                  <span>{tag}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="" style={{color : "var(--text-secondary-color)"}}>No tags found.</p>
          )}
        </Modal.Body>
        <Modal.Footer className="d-flex justify-content-between w-100">
        <Button
          variant="primary"
          onClick={() => {
            if (selectedTag) {
              setFilterState({ type: "ByTag", tag: selectedTag });
            } else {
              setFilterState(null); // ← No tag selected, remove filter
            }
            setShowTagModal(false);
          }}
        >
          Filter
        </Button>
        <Button
          variant="secondary"
          onClick={() => {
            setSelectedTag(null);
            setShowTagModal(false);
          }}
        >
          Close
        </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}