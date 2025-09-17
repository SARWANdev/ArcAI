import { Button } from "react-bootstrap";
import axios from "axios";
import { useAuth } from "../Contexts/AuthContext";
import { useState } from "react";
import { useProjects } from "../Contexts/ProjectsContext";
import "./DeleteButton.css";

export default function DeleteButton({
  project_id,
  document_id,
  conversation_id,
  onCloseSettings,
  onDelete, // callback to notify parent
}) {
  const { projectCount, setProjectCount, documentCount, setDocumentCount } = useProjects();
  const { sub } = useAuth();
  const [deleting, setDeleting] = useState(false);
  const [deleted, setDeleted] = useState(false);
    // State for the error popup
  const [errorMessage, setErrorMessage] = useState(null);

  async function handleDeleteProject() {
    try {
      setDeleting(true);
      setDeleted(false);
      await axios.delete("http://localhost:3000/library/delete-project", {
        data: { user_id: sub, project_id },
        withCredentials: true,
        headers: { "Content-Type": "application/json" },
      });
      setProjectCount(projectCount - 1);
      onCloseSettings?.();
      onDelete?.();
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to delete project");
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setDeleting(false);
    }
  }

  async function handleDeleteDocument() {
    try {
      setDeleting(true);
      setDeleted(false);
      await axios.delete("http://localhost:3000/document/delete", {
        data: { user_id: sub, project_id, document_id },
        withCredentials: true,
        headers: { "Content-Type": "application/json" },
      });
      setDocumentCount(documentCount - 1);
      onCloseSettings?.();
      onDelete?.();
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to delete document");
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setDeleting(false);
    }
  }

  async function handleDeleteConversation() {
    try {
      setDeleting(true);
      setDeleted(false);
      await axios.delete("http://localhost:3000/chat/delete", {
        data: { user_id: sub, conversation_id },
        withCredentials: true,
        headers: { "Content-Type": "application/json" },
      });
      onCloseSettings?.();
      onDelete?.();
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to delete conversation");
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setDeleting(false);
    }
  }

  function handleDelete() {
    if (conversation_id != null) {
      handleDeleteConversation();
    } else if (project_id != null && document_id == null) {
      handleDeleteProject();
    } else if (document_id != null) {
      handleDeleteDocument();
    } else {
      console.warn("No valid target to delete.");
    }
  }

  return (
    <>
    {/* The error popup element */}
    {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
      <Button className="fw-bold w-100 mb-1" id="delete-button" onClick={handleDelete}>
      {deleting
        ? "Deleting\n..."
        : deleted
        ? "Deleted\n✓"
        : "Delete"}
    </Button>
    </>
    
  );
}
