import PropTypes from "prop-types";
import { useState, useContext, useEffect } from "react";
import { Button, Modal } from "react-bootstrap";
import axios from "axios";
import { useAuth } from "../Contexts/AuthContext";
import { ThemeContext } from "../Contexts/ThemeContext";
import { createPortal } from "react-dom";
import "./NotepadToggleButton.css";

export default function NotepadToggleButton({
  document_id,
  showNotepad,
  setShowNotepad,
  setShowAIChat,
  noteText,
  setNoteText,
  savedText,
  setSavedText,
  fetchNote,
}) {
  const { sub: user_id } = useAuth();
  const { theme } = useContext(ThemeContext);

  const [showNotification, setShowNotification] = useState(false);
  const [notificationVisible, setNotificationVisible] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [pendingAction, setPendingAction] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  const saveNoteToDocument = async () => {
    try {
      if (!user_id || !document_id) return;
      await axios.post(
        "http://localhost:3000/document/note",
        { user_id, document_id, note: noteText },
        { withCredentials: true }
      );
      setShowNotification(true);
      setTimeout(() => setNotificationVisible(true), 10);
      setTimeout(() => setNotificationVisible(false), 2800);
      setTimeout(() => setShowNotification(false), 3300);
    } catch (err) {
      setErrorMessage(err.response?.data?.error || "Error saving note");
      setTimeout(() => setErrorMessage(null), 5000);
    }
  };

  const performAction = (action, callback = () => {}) => {
    if (action === "close") {
      setShowNotepad(false);
    } else if (action === "gotochat") {
      setShowNotepad(false);
      setShowAIChat(true);
    }
    setPendingAction(null);
    callback();
  };

  const requestClose = (action, callback = () => {}) => {
    const dirty = noteText !== savedText;
    if (dirty) {
      setPendingAction(action);
      setShowConfirm(true);
    } else {
      performAction(action, callback);
    }
  };

  const handleToggleNotepad = async () => {
    const toggled = !showNotepad;
    if (toggled) {
      setShowNotepad(true);
      await fetchNote();
    } else {
      requestClose("close");
    }
  };

  const handleSaveNote = async () => {
    try {
      setSaving(true);
      await saveNoteToDocument();
      setSavedText(noteText);
      setShowNotepad(false);
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    requestClose("close");
  };

  const handleGoToChat = () => {
    requestClose("gotochat");
  };

  const confirmSaveAndProceed = async () => {
    try {
      setSaving(true);
      await saveNoteToDocument();
      setSavedText(noteText);
      setShowConfirm(false);
      performAction(pendingAction || "close");
    } finally {
      setSaving(false);
    }
  };

  const discardChangesAndProceed = () => {
    setNoteText(savedText);
    setShowConfirm(false);
    performAction(pendingAction || "close");
  };

  const keepEditing = () => setShowConfirm(false);

  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape" && showNotepad) {
        requestClose("close");
      }
    };
    window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, [showNotepad, noteText, savedText]);

  return (
    <>
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
      <Button
        onClick={handleToggleNotepad}
        className="fw-bold"
        aria-label={showNotepad ? "Close notepad" : "Open notepad"}
        style={{
          position: "fixed",
          top: "19%",
          right: showNotepad ? "330px" : "10px",
          transform: "translateY(-50%)",
          zIndex: 1050,
          transition: "right 0.3s ease",
        }}
      >
        {showNotepad ? "→" : "📝 Notes"}
      </Button>
      <div
        style={{
          position: "fixed",
          top: 0,
          right: showNotepad ? 0 : "-340px",
          width: "340px",
          height: "100vh",
          backgroundColor: "var(--bg-color)",
          borderLeft: "1px solid #ccc",
          padding: "1rem",
          boxShadow: "0 0 10px rgba(0,0,0,0.1)",
          zIndex: 1060,
          transition: "right 0.3s ease",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <h5 className="fw-bold mb-3" style={{ color: "var(--text-color)" }}>
          Notepad
        </h5>
        <textarea
          className="form-control"
          style={{
            resize: "none",
            backgroundColor: "var(--bg-color)",
            color: "var(--text-color)",
            flexGrow: 1,
            marginBottom: "1rem",
            '::placeholder': {
              color: 'var(--text-color)',
              opacity: 0.7,
            },
          }}
          value={noteText}
          onChange={(e) => setNoteText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && e.shiftKey) {
              e.preventDefault();
              handleSaveNote();
            }
          }}
          placeholder="Write your notes here..."
          aria-label="Notepad text area"
        />
        <div className="d-flex justify-content-between align-items-center">
          <Button variant="primary" onClick={handleGoToChat}>
            Go to chat
          </Button>
          <div className="d-flex gap-2">
            <Button variant="secondary" onClick={handleCancel}>Cancel</Button>
            <Button variant="primary" onClick={handleSaveNote} disabled={saving}>
              {saving ? "Saving..." : "Save"}
            </Button>
          </div>
        </div>
      </div>
      <Modal show={showConfirm} onHide={keepEditing} centered>
        <Modal.Header closeButton>
          <Modal.Title>Save changes?</Modal.Title>
        </Modal.Header>
        <div className="p-3">
          Do you want to save your note before leaving this panel?
        </div>
        <div className="d-flex justify-content-between align-items-center p-3 pt-0">
          <Button variant="secondary" onClick={keepEditing}>
            Keep Editing
          </Button>
          <div className="d-flex gap-2">
            <Button variant="outline-danger" onClick={discardChangesAndProceed}>
              Discard Changes
            </Button>
            <Button variant="primary" onClick={confirmSaveAndProceed} disabled={saving}>
              {saving ? "Saving..." : "Save & Continue"}
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
}

NotepadToggleButton.propTypes = {
  document_id: PropTypes.string,
  showNotepad: PropTypes.bool.isRequired,
  setShowNotepad: PropTypes.func.isRequired,
  setShowAIChat: PropTypes.func.isRequired,
  noteText: PropTypes.string.isRequired,
  setNoteText: PropTypes.func.isRequired,
  savedText: PropTypes.string.isRequired,
  setSavedText: PropTypes.func.isRequired,
  fetchNote: PropTypes.func.isRequired,
};