import { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import axios from "axios";

// Predefined list of tag colors available for selection
const tagColors = [
  "#B0ABAA", "#E097BF", "#A38DD6", "#69BCD8",
  "#51B27C", "#FBE675", "#ED974F", "#DB5E52"
];

export default function TagManager({ user_id, document, refreshDocuments }) {
  // State to control whether the tag creation modal is open
  const [openTagModal, setOpenTagModal] = useState(false);
  // The current input value for the tag name
  const [tagName, setTagName] = useState("");
  // Currently selected color for the tag (starts as null - no color selected)
  const [selectedColor, setSelectedColor] = useState(null);
  // Controls visibility of modal for fade-in/out effect
  const [modalVisible, setModalVisible] = useState(false);
    // State for the error popup
  const [errorMessage, setErrorMessage] = useState(null);
  // State to track if user has attempted to submit without color
  const [showColorWarning, setShowColorWarning] = useState(false);

  // Effect to handle closing modal when ESC key is pressed
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape' && openTagModal) {
        handleCloseModal();
      }
    };

    if (openTagModal) {
      window.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [openTagModal]);

  // Effect to trigger fade-in and fade-out of modal using modalVisible state
  useEffect(() => {
    if (openTagModal) {
      // Delay to trigger CSS transition (fade in)
      setTimeout(() => setModalVisible(true), 10);
    } else {
      // Immediately start fade out
      setModalVisible(false);
    }
  }, [openTagModal]);

  // Open modal handler
  function handleOpenModal() {
    setOpenTagModal(true);
  }

  // Close modal handler with fade-out delay to match CSS transition duration
  function handleCloseModal() {
    setModalVisible(false);
    setTimeout(() => setOpenTagModal(false), 350); // match CSS transition duration
  }

  // Async function to create a new tag on the server
  async function makeTag() {
    // Client-side validation
    if (!tagName.trim()) {
      setErrorMessage("Please enter a tag name");
      setTimeout(() => setErrorMessage(null), 5000);
      return;
    }
    
    if (!selectedColor) {
      setShowColorWarning(true);
      setTimeout(() => setShowColorWarning(false), 5000);
      return;
    }

    try {
      await axios.post(
        "http://localhost:3000/document/tag",
        {
          user_id,
          document_id: document.DocumentId,
          tag_name: tagName,
          selected_colour: selectedColor,
        },
        { withCredentials: true }
      );

      await refreshDocuments();
      // Only close modal and reset fields on success
      setOpenTagModal(false);
      setTagName("");
      setSelectedColor(null);
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to create tag.");
      setTimeout(() => setErrorMessage(null), 5000);
      // Don't close modal or reset fields on error - let user see the error and fix it
    }
  }

  // Async function to remove an existing tag on the server
  async function removeTag() {
    try {
      await axios.delete(
        "http://localhost:3000/document/tag",
        {
          data: {
            user_id,
            document_id: document.DocumentId,
          },
          withCredentials: true,
        }
      );

      await refreshDocuments();
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to remove tag.");
      setTimeout(() => setErrorMessage(null), 5000);
    }
  }

  return (
    <>
      {/* The error popup element */}
      {errorMessage && (
        <div className="error-popup" style={{ zIndex: 9999 }}>
          <p>{errorMessage}</p>
        </div>
      )}
      {/* Show disabled button if tag already exists */}
      
      {document.TagName ? (
        <Button
          id="tag-added-button"
          disabled
          style={{
            fontWeight: "bold",
            color: document.TagColor || "var(--text-color)",
            backgroundColor: "var(--bg-button-color)",
            border: "1px solid var(--text-secondary-color)",
            marginBottom: "5px",
          }}
        >
          ✓ {document.TagName}
        </Button>
      ) : (
        // Show add tag button if no tag exists
        <Button
          id="add-tag-button"
          onClick={handleOpenModal}
          style={{
            backgroundColor: "var(--bg-button-color)",
            color: "var(--text-color)",
            borderColor: "var(--text-secondary-color)",
            marginBottom: "5px",
          }}
        >
          + Add Tag
        </Button>
      )}

      {/* Show remove tag button only if tag exists */}
      {document.TagName && (
        <Button
          id="remove-tag-button"
          onClick={removeTag}
          style={{
            backgroundColor: "var(--bg-button-color)",
            color: "var(--text-color)",
            borderColor: "var(--text-secondary-color)",
            marginBottom: "5px",
          }}
        >
          Remove Tag
        </Button>
      )}

      {/* Modal for creating a new tag */}
      {openTagModal && (
        <div
          className="modal d-block"
          tabIndex="-1"
          role="dialog"
          onClick={handleCloseModal} // clicking outside modal closes it
          style={{
            backgroundColor: "rgba(0, 0, 0, 0.5)",
            opacity: modalVisible ? 1 : 0,
            transition: "opacity 0.35s",
            zIndex: 9998,
          }}
        >
          <div
            className="modal-dialog"
            role="document"
            onClick={(e) => e.stopPropagation()} // prevent closing modal when clicking inside
            style={{
              transform: modalVisible ? "scale(1)" : "scale(0.97)",
              transition: "transform 0.35s",
            }}
          >
            <div
              className="modal-content"
              style={{
                backgroundColor: "var(--bg-color)",
                color: "var(--text-color)",
                boxShadow: modalVisible ? "0 8px 32px rgba(0,0,0,0.25)" : "none",
                transition: "box-shadow 0.35s",
              }}
            >
              <div
                className="modal-header"
                style={{ borderBottom: "1px solid var(--text-secondary-color)" }}
              >
                <h5 className="modal-title">Create Tag</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setOpenTagModal(false)}
                  aria-label="Close"
                />
              </div>

              <div className="modal-body">
                {/* Tag name input */}
                <input
                  type="text"
                  className="form-control mb-3"
                  placeholder="Enter tag name"
                  value={tagName}
                  onChange={(e) => setTagName(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && tagName.trim() && selectedColor) {
                      makeTag();
                    }
                  }}
                  style={{
                    backgroundColor: "var(--bg-button-color)",
                    color: "var(--text-color)",
                    borderColor: "var(--text-secondary-color)",
                  }}
                />

                {/* Color selection */}
                <div className="mt-3">
                  <label className="form-label d-block">Select Tag Color:</label>
                  <div className="d-flex gap-2 flex-wrap">
                    {tagColors.map((color) => (
                      <button
                        key={color}
                        type="button"
                        className={`rounded-circle border ${
                          selectedColor === color ? "border-dark border-3" : "border-1"
                        }`}
                        onClick={() => {
                          setSelectedColor(color);
                          setShowColorWarning(false); // Hide warning when color is selected
                        }}
                        style={{
                          width: "30px",
                          height: "30px",
                          backgroundColor: color,
                          outline: "none",
                          cursor: "pointer",
                          borderColor: "var(--text-secondary-color)",
                        }}
                      />
                    ))}
                  </div>
                  {showColorWarning && (
                    <div className="text-danger mt-2" style={{ fontSize: "0.875rem" }}>
                      ⚠️ Please select a color for your tag
                    </div>
                  )}
                </div>
              </div>

              <div
                className="modal-footer"
                style={{ borderTop: "1px solid var(--text-secondary-color)" }}
              >
                {/* Cancel button */}
                <Button
                  variant="secondary"
                  onClick={() => setOpenTagModal(false)}
                  style={{
                    backgroundColor: "#70747c",
                    color: "white",
                    borderColor: "var(--text-secondary-color)",
                  }}
                >
                  Cancel
                </Button>

                {/* Create tag button */}
                <Button
                  variant="primary"
                  onClick={makeTag}
                  disabled={!tagName.trim() || !selectedColor}
                  style={{
                    backgroundColor: "#0069d9",
                    color: "white",
                    borderColor: "var(--bg-login-button-color)",
                  }}
                >
                  Create
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}