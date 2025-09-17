import PropTypes from "prop-types";
import { Button, Modal, Form } from "react-bootstrap";
import { useState, useEffect } from "react";
import { useAuth } from "../Contexts/AuthContext";
import axios from "axios";
import { createPortal } from "react-dom";
import "./RenameButton.css";

/**
 * RenameButton handles renaming of projects, documents, or conversations.
 * Props are used to determine the target and callbacks for modal state and refresh.
 */
export default function RenameButton({
  project_id,
  project_title,
  document_id,
  document_title,
  conversation_id,
  conversation_title,
  onRename,
  onOpenModal,
  onCloseModal,
  refreshDocuments,
}) {
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState(
    project_title ?? document_title ?? conversation_title ?? ""
  );
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const { sub } = useAuth();

  // Update name when any title prop changes
  useEffect(() => {
    setName(project_title ?? document_title ?? conversation_title ?? "");
  }, [project_title, document_title, conversation_title]);

  // Handler to show modal
  const handleShowModal = () => {
    setShowModal(true);
    setError(""); // Clear any previous errors
    onOpenModal?.();
  };

  // Handler to close modal
  const handleCloseModal = () => {
    setShowModal(false);
    setError(""); // Clear errors when closing
    onCloseModal?.();
  };

  // Handler for renaming
  const handleRename = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      setError(""); // Clear any previous errors
      
      if (project_id) {
        await axios.patch(
          "http://localhost:3000/library/rename-project",
          { user_id: sub, project_id, name: name || "Untitled Project" },
          { withCredentials: true, headers: { "Content-Type": "application/json" } }
        );
      } else if (document_id) {
        await axios.patch(
          "http://localhost:3000/project/rename",
          { user_id: sub, document_id, name: name || "Untitled Document" },
          { withCredentials: true, headers: { "Content-Type": "application/json" } }
        );
      } else if (conversation_id) {
        await axios.patch(
          "http://localhost:3000/chat/rename",
          { user_id: sub, conversation_id, name: name || "Untitled Conversation" },
          { withCredentials: true, headers: { "Content-Type": "application/json" } }
        );
      } else {
        console.warn("No target ID provided for renaming.");
        return;
      }
      
      if (refreshDocuments) {
        refreshDocuments();
      }
      onRename?.();
      handleCloseModal();
    } catch (err) {
      console.error("Rename failed:", err.response?.data || err.message);
      
      // Extract error message from backend response
      let errorMessage = "Failed to rename. Please try again.";
      
      if (err.response?.data?.error) {
        // Use the error message from the backend
        errorMessage = err.response.data.error;
      }
      
      setError(errorMessage);
      // Auto-hide error after 5 seconds
      setTimeout(() => setError(""), 5000);
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      {/* Error Popup - Rendered at document body level */}
      {error && createPortal(
        <div className="error-popup">
          <p>{error}</p>
        </div>,
        document.body
      )}
      
      <Button
        className="fw-bold w-100"
        onClick={handleShowModal}
        id="rename-button"
        aria-label="Rename"
      >
        Rename
      </Button>

      <Modal show={showModal} onHide={handleCloseModal} centered>
        <Modal.Header closeButton>
          <Modal.Title>Rename</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleRename}>
            <Form.Group controlId="renameNameInput" className="mb-3">
              <Form.Label>New name</Form.Label>
              <Form.Control
                type="text"
                value={name}
                style={{
                  backgroundColor: "var(--bg-color)", 
                  color: "var(--text-color)"
                }}
                onChange={(e) => setName(e.target.value)}
                autoFocus
                aria-label="New name"
                isInvalid={!!error}
              />
            </Form.Group>
            <div className="d-flex justify-content-end gap-2">
              <Button variant="secondary" onClick={handleCloseModal}>
                Cancel
              </Button>
              <Button 
                type="submit" 
                variant="primary" 
                disabled={saving || !name.trim()}
              >
                {saving ? "Saving..." : "Save"}
              </Button>
            </div>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
}

RenameButton.propTypes = {
  project_id: PropTypes.string,
  project_title: PropTypes.string,
  document_id: PropTypes.string,
  document_title: PropTypes.string,
  conversation_id: PropTypes.string,
  conversation_title: PropTypes.string,
  onRename: PropTypes.func,
  onOpenModal: PropTypes.func,
  onCloseModal: PropTypes.func,
  refreshDocuments: PropTypes.func,
};