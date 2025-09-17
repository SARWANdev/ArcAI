import { useState } from "react";
import { Button, Modal, Form } from "react-bootstrap";
import { useAuth } from "../Contexts/AuthContext";
import "./SetBibtexButton.css";
import axios from "axios";

/**
 * SetBibtexButton allows users to view and edit the BibTeX string associated with a document.
 *
 * Props:
 * - document_id: ID of the document whose BibTeX is being edited.
 * - refreshDocuments: Optional callback to refresh document list after saving.
 */
export default function SetBibtexButton({ document_id, refreshDocuments }) {
  const { sub } = useAuth(); // Get user ID from auth context

  // Modal visibility state
  const [show, setShow] = useState(false);

  // State to hold the BibTeX string
  const [bibtex, setBibtex] = useState("");

  // Closes the modal
  const handleClose = () => setShow(false);
  const [errorMessage, setErrorMessage] = useState(null);

  // Opens the modal and fetches the current BibTeX string
  const handleShow = async () => {
    try {
      const response = await axios.get("http://localhost:3000/document/bibtex/string", {
        params: {
          userid: sub,
          document_id,
        },
      });

      // Populate BibTeX state with response or empty string
      setBibtex(response.data.data?.BibTeX || "");
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Error fetching bibtex");
      setTimeout(() => setErrorMessage(null), 5000);
      setBibtex("");
    }

    // Show the modal
    setShow(true);
  };

  // Saves the updated BibTeX string to the backend
  const handleSave = async () => {
    try {
      await axios.post("http://localhost:3000/document/bibtex/set", {
        userid: sub,
        document_id,
        bibtex,
      });

      handleClose(); // Close modal after save

      // Refresh document list if provided
      if (refreshDocuments) {
        refreshDocuments();
      }
    } catch (err) {
      console.error("Error saving BibTeX:", err);
    }
  };

  // Handle keydown events in the textarea
  const handleKeyDown = (e) => {
    // Check if Shift + Enter is pressed
    if (e.key === "Enter" && e.shiftKey) {
      e.preventDefault(); // Prevent default behavior (new line)
      handleSave(); // Trigger save
    }
  };

  return (
    <>
    {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
      {/* Button to open modal */}
      <Button
        id="set-bibtex-button"
        className="btn btn-light"
        onClick={handleShow}
      >
        Set Bibtex
      </Button>

      {/* Modal for editing BibTeX */}
      <Modal show={show} onHide={handleClose} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Set Bibtex</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <Form.Control
            as="textarea"
            rows={6}
            placeholder="Enter BibTeX"
            value={bibtex}
            onChange={(e) => setBibtex(e.target.value)}
            onKeyDown={handleKeyDown} // Add keydown handler
            style={{ resize: "vertical",
              backgroundColor: "var(--bg-color)", 
              color: "var(--text-color)"
            }}
          />
          <div className="text-muted mt-2 small">
            Press Shift + Enter to save
          </div>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSave}>
            Save
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}