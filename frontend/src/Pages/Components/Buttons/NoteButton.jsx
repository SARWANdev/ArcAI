import PropTypes from "prop-types";
import { useState, useEffect, useContext } from "react";
import { Button, Modal, Form } from "react-bootstrap";
import { useAuth } from "../Contexts/AuthContext";
import axios from "axios";
import { ThemeContext } from "../Contexts/ThemeContext";
import { createPortal } from "react-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "./NoteButton.css";

/**
 * NoteButton opens a modal for editing and saving notes for a project or document.
 * @param {string} project_id - The project ID for the note context.
 * @param {string} document_id - The document ID for the note context.
 * @param {string} user_id - The user ID (optional, will use AuthContext if not provided).
 */
export default function NoteButton({ project_id, document_id, user_id }) {
  const { sub } = useAuth(); // Authenticated user ID from context
  const { theme } = useContext(ThemeContext); // Current theme from context

  // Local state management
  const [show, setShow] = useState(false); // Controls modal visibility
  const [note, setNote] = useState(""); // Stores current note content
  const [originalNote, setOriginalNote] = useState(""); // Last saved version
  const [saving, setSaving] = useState(false); // True while saving

  const [showConfirm, setShowConfirm] = useState(false); // Show confirmation when closing unsaved
  const [showNotification, setShowNotification] = useState(false); // Show/hide notification box
  const [notificationVisible, setNotificationVisible] = useState(false); // Controls fade-in/out of notification
  const [errorMessage, setErrorMessage] = useState(null);

  // Show modal
  const handleShowModal = () => setShow(true);

  // Ask for confirmation before closing if there are unsaved changes
  const requestCloseModal = () => {
    const hasUnsavedChanges = note !== originalNote;
    if (hasUnsavedChanges) {
      setShowConfirm(true);
    } else {
      setShow(false);
    }
  };

  // Force close modal and confirmation without saving
  const handleCloseModalHard = () => {
    setShow(false);
    setShowConfirm(false);
  };

  // Save note to backend based on context
  const handleSaveNote = async () => {
    try {
      setSaving(true);
      if (document_id == null && project_id != null) {
        await saveNoteToProject(); // Save to project note
      } else if (project_id == null && document_id != null) {
        await saveNoteToDocument(); // Save to document note
      }

      setOriginalNote(note); // Update last saved

      // Show notification with fade-in/out
      setShowNotification(true);
      setTimeout(() => setNotificationVisible(true), 10);
      setTimeout(() => setNotificationVisible(false), 2800);
      setTimeout(() => setShowNotification(false), 3300);

      handleCloseModalHard(); // Close modal after save
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Error saving note");
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setSaving(false);
    }
  };

  // Confirmation modal actions
  const confirmSaveAndClose = async () => {
    await handleSaveNote();
  };
  const discardAndClose = () => {
    setNote(originalNote); // Reset note back to last saved version
    handleCloseModalHard();
  };
  const continueEditing = () => setShowConfirm(false);

  // Save note to project endpoint
  const saveNoteToProject = async () => {
    await axios.post(
      "http://localhost:3000/project/note",
      {
        user_id: sub,
        project_id,
        note,
      },
      { withCredentials: true }
    );
  };

  // Save note to document endpoint
  const saveNoteToDocument = async () => {
    await axios.post(
      "http://localhost:3000/document/note",
      {
        user_id: user_id || sub,
        document_id,
        note,
      },
      { withCredentials: true }
    );
  };

  // Fetch note when modal opens
  useEffect(() => {
    if (!show) return;

    async function fetchNote() {
      try {
        let response;
        if (document_id == null && project_id != null) {
          // Fetch project note
          response = await axios.get("http://localhost:3000/project/note", {
            params: { user_id: sub, project_id },
            withCredentials: true,
          });
        } else if (project_id == null && document_id != null) {
          // Fetch document note
          response = await axios.get("http://localhost:3000/document/note", {
            params: { user_id: user_id || sub, document_id },
            withCredentials: true,
          });
        }

        const fetchedNote = response?.data?.note ?? "";
        setNote(fetchedNote);
        setOriginalNote(fetchedNote);
      } catch (err) {
        setErrorMessage(err.response?.data?.error|| "Error retrieving note");
        setTimeout(() => setErrorMessage(null), 5000);
        setNote("");
        setOriginalNote("");
      }
    }

    fetchNote();
  }, [show, project_id, document_id, user_id, sub]);

  return (
    <>
      {/* Error Popup - Rendered at document body level */}
      {errorMessage && createPortal(
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>,
        document.body
      )}
      {showNotification && (
        <div
          style={{
            position: 'fixed',
            top: 24,
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'var(--bg-login-button-color)',
            color: '#fff',
            padding: '2rem 3.5rem',
            borderRadius: '16px',
            fontSize: '1.5rem',
            boxShadow: '0 4px 24px rgba(0,0,0,0.25)',
            zIndex: 9999,
            fontWeight: 'bold',
            border: 'none',
            transition: 'opacity 0.5s',
            opacity: notificationVisible ? 1 : 0,
            pointerEvents: 'none',
          }}
          aria-live="polite"
        >
          Notepad saved!
        </div>
      )}

      {/* Open modal button */}
      <Button
        className="w-150"
        id="note-button"
        onClick={handleShowModal}
        aria-label="Open Notepad"
      >
        Open Notepad
      </Button>

      {/* Modal content */}
      <Modal show={show} onHide={requestCloseModal} centered size="lg" style={{ color: "var(--text-color)" }}>
        <Modal.Header closeButton style={{ backgroundColor: "var(--bg-color)", color: "var(--text-color)" }}>
          <Modal.Title>Notepad</Modal.Title>
        </Modal.Header>

        <Modal.Body style={{ backgroundColor: "var(--bg-color)", color: "var(--text-color)" }}>
          <Form.Control
            id="input-text"
            as="textarea"
            rows={10}
            style={{
              backgroundColor: "var(--bg-color)",
              color: "var(--text-color)",
              overflow: "auto",
            }}
            value={note}
            onChange={(e) => setNote(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && e.shiftKey) {
                e.preventDefault(); // Prevent newline on Shift+Enter
                handleSaveNote();   // Save note instead
              }
            }}
            placeholder="Write your notes here..."
            aria-label="Notepad text area"
          />
        </Modal.Body>

        <Modal.Footer style={{ backgroundColor: "var(--bg-color)", color: "var(--text-color)" }}>
          <Button variant="secondary" onClick={requestCloseModal}>
            Cancel
          </Button>
          <Button variant="success" onClick={handleSaveNote} disabled={saving}>
            {saving ? "Saving..." : "Save Note"}
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Confirmation modal for unsaved changes */}
      <Modal show={showConfirm} onHide={continueEditing} centered>
        <Modal.Header closeButton>
          <Modal.Title>Save changes?</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Do you want to save your note before closing?
        </Modal.Body>
        <Modal.Footer className="d-flex justify-content-between w-100">
          <Button variant="secondary" onClick={continueEditing}>
            Keep Editing
          </Button>
          <div className="d-flex gap-2">
            <Button variant="outline-danger" onClick={discardAndClose}>
              Discard Changes
            </Button>
            <Button variant="primary" onClick={confirmSaveAndClose} disabled={saving}>
              {saving ? "Saving..." : "Save & Close"}
            </Button>
          </div>
        </Modal.Footer>
      </Modal>
    </>
  );
}

// Define expected prop types for the component
NoteButton.propTypes = {
  project_id: PropTypes.string,
  document_id: PropTypes.string,
  user_id: PropTypes.string,
};
