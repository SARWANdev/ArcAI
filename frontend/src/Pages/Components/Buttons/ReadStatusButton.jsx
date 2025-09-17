// ReadStatusButton.js

import { Button } from "react-bootstrap";
import axios from "axios";
import { useState } from "react";

/**
 * ReadStatusButton toggles the read/unread status of a document for a user.
 * 
 * Props:
 * - user_id: ID of the user
 * - project_id: ID of the parent project
 * - document_id: ID of the target document
 * - isRead: current read status (boolean)
 * - onChange: callback to notify parent of status change
 */
export default function ReadStatusButton({ 
  user_id, 
  project_id, 
  document_id, 
  isRead, 
  onChange 
}) {
  // Loading state to prevent multiple rapid clicks
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  /**
   * Handles toggling read/unread state by sending
   * POST (mark as read) or DELETE (mark as unread) request to backend.
   */
  async function toggleReadStatus() {
    try {
      setLoading(true); // Begin loading

      if (isRead) {
        // If currently marked as read, delete read status
        await axios.delete("http://localhost:3000/document/read", {
          data: { user_id, project_id, document_id },
          withCredentials: true,
        });
        onChange(false); // Inform parent that it's now unread
      } else {
        // If currently unread, mark as read
        await axios.post(
          "http://localhost:3000/document/read",
          { user_id, project_id, document_id },
          { withCredentials: true }
        );
        onChange(true); // Inform parent that it's now read
      }

    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Error toggling read status");
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setLoading(false); // End loading
    }
  }

  return (
    <>
    {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
    <Button
      id="mark-as-read-button"
      onClick={toggleReadStatus}
      disabled={loading} // Disable while loading
      style={{
        fontSize: "16px",
        color: isRead ? "green" : "var(--text-color)", // Green if read
        fontWeight: "bold",
        textDecoration: "none",
        fontStyle: isRead ? "italic" : "normal",
      }}
    >
      {/* Text content based on read status */}
      {isRead ? "✓ Read" : "Mark as read"}
    </Button>
    </>
  );
}